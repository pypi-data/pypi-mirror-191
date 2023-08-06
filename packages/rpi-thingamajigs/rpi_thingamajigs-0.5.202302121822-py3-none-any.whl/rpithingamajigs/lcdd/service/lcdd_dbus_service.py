"""The LCDD Dbus service."""

from pydbus import SystemBus, SessionBus

class LcddDbusService(object):
    """
        <node>
        <interface name='org.hackerbuero.LCDD.v1'>
            <method name='Dimensions'>
            <arg type='i' name='columns' direction='out'/>
            <arg type='i' name='rows' direction='out'/>
            </method>
            <method name='Message'>
            <arg type='as' name='lines' direction='in'/>
            <arg type='i' name='duration' direction='in'/>
            <arg type='s' name='response' direction='out'/>
            </method>
            <method name='Clear'>
            <arg type='s' name='response' direction='out'/>
            </method>
        </interface>
        </node>
    """

    def __init__(self, lcdd):
        assert lcdd is not None
        self._lcdd = lcdd
    
    @classmethod
    def service_name(cls):
        """Return the DBUS service name to be exposed. This should match the XML specification above!"""
        return "org.hackerbuero.LCDD.v1"

    def lcdd(self):
        assert self._lcdd is not None
        return self._lcdd
            
    def Dimensions(self):
        """Return the display dimensions as columns and rows."""
        return self.lcdd().display().dimensions()
    
    def Message(self, lines, duration):
        self.lcdd().message(lines, duration)
        return "Ok"

    def Clear(self):
        """Clear the display. Deletes the current and all pending messages."""
        self.lcdd().clear()
        return "Ok"
