# The Knust service is a long-running program that manages the 
# Knust thermostat hardware. Clients interact with it using DBUS.

from pydbus import SystemBus, SessionBus
import signal
from knust_service.session import Session
import logging

from knust_service.string_format_helpers import hhmm, temperature_5_digits, dt_string

def _log():
    return logging.getLogger('KnustDbusService')

class KnustDbusService(object):
    """
        <node>
        <interface name='org.hackerbuero.KnustService.v5'>
            <method name='Status'>
            <arg type='as' name='response' direction='out'/>
            </method>
            <method name='AddSession'>
            <arg type='d' name='target_temp' direction='in'/>
            <arg type='u' name='duration' direction='in'/>
            <arg type='s' name='response' direction='out'/>
            </method>
            <method name='DropSession'>
            <arg type='s' name='response' direction='out'/>
            </method>
            <method name='Quit'>
            <arg type='s' name='response' direction='out'/>
            </method>
        </interface>
        </node>
    """

    KnustDbusServiceName = 'org.hackerbuero.KnustService.v5'

    def __init__(self, knustservice):
        assert knustservice != None
        self._service = knustservice

    def publish(self, sessionBus):
        bus = SessionBus() if sessionBus else SystemBus()
        bus.publish(KnustDbusService.KnustDbusServiceName, self)

    def service(self):
        return self._service


    def Status(self):
        """Return the current status of the device."""
        _log().debug("Status report requested...")
        lines = []
        for session in self.service().sessions():
            if session.status in [Session.Status.DROPPED, Session.Status.COMPLETED]:
                pass
            elif session.status == Session.Status.STARTED:
                lines.append("STARTED: {}C / {} (active since {})".format(temperature_5_digits(session.target_temperature), hhmm(session.duration), dt_string(session.start_time)))
            else:
                lines.append("WAITING: {}C / {}".format(temperature_5_digits(session.target_temperature), hhmm(session.duration)))
        if not lines:
            lines.append("No active sessions.")
        return lines

    def AddSession(self, target_temp, duration):
        """Add a session with the specified target_temp temperature (Celsius) and duration (seconds)."""
        _log().debug("New session: target {}, duration {}.".format(target_temp, duration))
        try:
            self.service().add_session(Session(None, duration, target_temp))
            return "Ok"
        except Exception as e:
            return "Error: {}".format(str(e))

    def DropSession(self):
        _log().debug("Dropping current session...")
        if self.service().drop_active_session():
            return "Current session dropped."
        else:
            return "No current session."

    def Quit(self):
        _log().debug("Quit requested, service terminating...")
        self.service().quit()
        return 'Quit requested, service terminating...'
