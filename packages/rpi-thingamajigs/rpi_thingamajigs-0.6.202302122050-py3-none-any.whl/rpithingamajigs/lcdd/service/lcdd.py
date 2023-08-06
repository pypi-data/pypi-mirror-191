from pydbus import SystemBus, SessionBus
from pydbus.generic import signal
import signal
from gi.repository import GLib, GObject
import logging
from rpithingamajigs.lcdd.service.lcdd_dbus_service import LcddDbusService

class _Message():
    def __init__(self, lines, duration, min_duration):
        self._lines = lines
        self._remainder = duration
        self._min_remainder = min_duration

    def lines(self):
        return self._lines

    def minimum_duration_has_expired(self):
        return self._min_remainder <=0

    def duration_has_expired(self):
        return self._remainder <= 0

    def countdown_to_expiration(self):
        self._remainder = self._remainder-1
        self._min_remainder = self._min_remainder-1

class LCDD():
    def __init__(self, configuration):
        assert configuration != None
        self._configuration = configuration
        self._display = self.configuration().display()
        self._service = LcddDbusService(self)
        self._messages = []
        self._current = None
        self.__loop = GLib.MainLoop()

    def configuration(self):
        assert self._configuration != None
        return self._configuration

    def display(self):
        assert self._display != None
        return self._display

    def message(self, lines, duration):
        message = _Message(lines, duration, self.configuration().minimum_timeout())
        self._messages.append(message)

    def clear(self):
        self._messages = []
        self._current = None
        self.display().clear()

    def service(self):
        assert self._service != None
        return self._service

    def _loop(self):
        assert self.__loop != None
        return self.__loop

    def _display_tick(self):
        # logging.info('tick ... tock...')
        if self._current:
            self._current.countdown_to_expiration()
            if self._current.minimum_duration_has_expired() and self._messages:
                # minimum duration has expired and there are other messages pending, next!
                self._current = None
            elif self._current.duration_has_expired():
                # the message has expired
                self._current = None
                if not self._messages:
                    self.display().clear()
            else:
                return True

        assert self._current == None
        if self._messages:
            self._current = self._messages.pop(0)
            self.display().message(self._current.lines())
        return True

    def sigterm_handler(self):
        logging.info('Received SIGTERM, terminating...')
        self.quit()

    def quit(self):
        if self.configuration().farewell():
            self.display().message( [self.configuration().farewell() ] )
        self._loop().quit()

    def run(self):
        bus = SessionBus() if self.configuration().use_sessionbus() else SystemBus()
        GObject.timeout_add_seconds(1, self._display_tick)
        bus.publish(self.service().service_name(), self.service())
        GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, self.sigterm_handler)
        if self.configuration().motd():
            self.message([self.configuration().motd()], 3)
        self._loop().run()
