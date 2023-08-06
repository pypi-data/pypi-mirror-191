"""A client class for the LCDD display manager service."""

from pydbus import SessionBus, SystemBus
from rpithingamajigs.lcdd.service.lcdd_dbus_service import LcddDbusService
from gi.repository import GLib, GObject

class LcddClient():
    def __init__(self):
        self._bus = None
        self._proxy = None

    def connect(self, use_sessionbus):
        self._bus = SessionBus() if use_sessionbus else SystemBus()
        try:
            self._proxy = self._bus.get(LcddDbusService.service_name())
        except GLib.Error as e:
            raise RuntimeError('Unable to connect to service: {}. Is this the correct bus?'.format(str(e)))

    def message(self, lines, duration=-1):
        assert self._proxy != None
        reply = self._proxy.Message( lines, duration )
        if reply != "Ok":
            print(reply)

    def clear(self):
        assert self._proxy != None
        reply = self._proxy.Clear()
        if reply != "Ok":
            print(reply)

    def dimensions(self):
        assert self._proxy != None
        columns, rows = self._proxy.Dimensions()
        return columns, rows

    def disconnect(self):
        self._proxy = None
        self._bus = None

    def is_connected(self):
        return self._proxy is not None

if __name__ == '__main__':
    client = LcddClient()
    client.connect(True)
    client.clear()
    print("{} columns / {} rows".format(*client.dimensions()))
    client.message( ["Hello, World!", "This is amazing!"], 5)
