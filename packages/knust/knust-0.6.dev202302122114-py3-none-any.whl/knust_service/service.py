# The Knust service.
import logging
from gi.repository import GLib, GObject
import signal
from datetime import datetime, timedelta
import json
import jsonpickle
import copy
import humanize

from rpithingamajigs.lcdd.client.ignorant_lcdd_client import IgnorantLcddClient

from knust_service.knust_dbus_service import KnustDbusService
from knust_service.hardware_interface import HardwareInterface
from knust_service import Session
from knust_service.string_format_helpers import hhmm, temperature_5_digits, dt_string

class KnustService:
    Interval = 10 # seconds between session ticks

    def __init__(self, mainloop, hardware, data_file_name = "test_sessions.json"):
        assert mainloop != None
        assert hardware is not None and isinstance(hardware, HardwareInterface)
        self._log = logging.getLogger('knustsrv')
        self._loop = mainloop
        self._hardware = hardware
        self._sessions = []
        self._last_persisted_sessions = None
        self._active_session = None
        self._dbus_service = KnustDbusService(self)
        self._data_file_name = data_file_name
        self._lcddc = IgnorantLcddClient()

    
    def log(self):
        assert self._log != None
        return self._log

    def dbus_service(self):
        return self._dbus_service

    def hardware(self):
        return self._hardware

    def lcddc(self):
        return self._lcddc

    def publish(self, sessionbus):
        self.dbus_service().publish(sessionbus)
        try:
            self._lcddc.connect(sessionbus)
        except RuntimeError:
            self.log().warning('Unable to connect LCDD client. Display will not be reachable for messages.')

    def status(self):
        """Return the current status of the device as a string."""
        return "All good."

    def add_session(self, session):
        '''Add a session.'''
        min_temperature = 0.0
        max_temperature = 50.0
        if session.duration is None or session.target_temperature is None:
            raise RuntimeError('Cannot add a session without a target temperature and a duration.')
        if session.target_temperature < min_temperature or session.target_temperature > max_temperature:
            raise RuntimeError('Unsuitable target temperature of {}°C (must be between {} and {}°C).'
                .format(session.target_temperature, min_temperature, max_temperature))
        if session.duration <= 0:
            raise RuntimeError('The session duration must be positive, not {}.'.format(session.duration))
        self._sessions.append(session)

    def sessions(self):
        return self._sessions

    def active_session(self):
        return self._active_session

    def drop_active_session(self):
        '''Drop the active session.'''
        if self.active_session():
            self.active_session().status = Session.Status.DROPPED
            return True
        return False

    def clear(self):
        '''Drop all sessions.'''

    def persist_sessions(self):
        '''persist_sessions saves the sessions into a data file in the current working directory.'''
        if self._last_persisted_sessions is not None and self._last_persisted_sessions == self.sessions():
            self.log().debug('persist_sessions: No change to sessions, skipping...')
        else:
            self.log().info('persisting sessions...')
            with open(self._data_file_name, 'w') as data_file:
                data = jsonpickle.encode(self.sessions(), indent=4)
                data_file.write(data)
                data_file.write('\n')
            self._last_persisted_sessions = copy.deepcopy(self.sessions())

    def restore_sessions(self):
        '''restore_sessions loads the persisted session state from the data file.'''
        try:
            with open(self._data_file_name, 'r') as data_file:
                data = jsonpickle.decode(data_file.read())
                self._sessions = data
                self._last_persisted_sessions = copy.deepcopy(data)
        except FileNotFoundError:
            # may happen if no sessions have been persisted before
            self.log().debug('No persisted session data found, first run (ignored)?')

    def maybe_reactivate_session(self):
        self.restore_sessions()
        for session in self.sessions():
            if session.status == Session.Status.STARTED:
                self.log().info('Resuming active session (started {}, {} total).'.format(dt_string(session.start_time), hhmm(session.duration)))
                self._active_session = session
                return
        self.log().debug('No session to resume.')

    def quit(self):
        '''Terminate the service. Beware that it may be restarted when running in systemd.'''
        self.log().info('Quit requested, terminating...')
        self._loop.quit()

    def _session_tick(self):
        """This method is called regularly by the main loop timer."""
        self.log().debug("tick tock...")
        try:
            now = datetime.now()
            if self.active_session():
                passed = round((now - self.active_session().start_time).total_seconds())
                self.log().debug('Session active since {} ({}).'.format(dt_string(self.active_session().start_time), hhmm(passed)))
                if passed >= self.active_session().duration:
                    self.log().info('Session completed ({}).'.format(hhmm(passed)))
                    self.active_session().status = Session.Status.COMPLETED
                    self._active_session = None
                elif self.active_session().status == Session.Status.DROPPED:
                    # the user requested the session to be dropped
                    self.log().info('Session dropped by the user after {}.'.format(hhmm(passed)))
                    self._active_session = None
                else:
                    return True # continue with session

            assert self.active_session() is None
            for session in self.sessions():
                if session.status == Session.Status.NEW:
                    session.status = Session.Status.STARTED
                    session.start_time = datetime.now()
                    self._active_session = session
                    break

            if self.active_session():
                self.log().info('Activated next session ({}, {}).'.format(self.active_session().target_temperature, hhmm(self.active_session().duration)))
            else:
                self.log().debug('No current session.')

            # True indicates that the timer should trigger again
            return True
        finally:
            heater = self._thermostat()
            self._post_session_status_message(heater)
            self.persist_sessions()

    def _thermostat(self):
        status = False
        try:
            if not self.active_session():
                self.log().debug('No active session, turning heater off...')
            else:
                spot = datetime.now()
                measurement = self.hardware().temperature_sensor.get_1min_average(spot)
                if measurement.is_valid():
                    status = measurement.temperature < self.active_session().target_temperature
            return status
        finally: # make sure the heater status is always set:
            self.hardware().set_heater_on(status)

    def _post_session_status_message(self, heater):
        # columns, rows = self.lcddc().dimensions()
        current_sessions = 0
        for session in self.sessions():
            if session.status not in [ Session.Status.COMPLETED, Session.Status.DROPPED]:
                current_sessions += 1
        now = datetime.now()
        measurement = self.hardware().temperature_sensor.get_1min_average(now)
        line2 = 'cur:{}C'.format(temperature_5_digits(measurement.temperature))

        if self.active_session():
            passed = round((now - self.active_session().start_time).total_seconds())
            remaining = self.active_session().duration - passed

            line1 = '{}/{}:{}C       {}'.format(
                '1' if self.active_session() else '-',
                current_sessions,
                temperature_5_digits(self.active_session().target_temperature),
                ' ON' if heater else 'OFF')
            line3 = 'dur: {}/{}'.format(hhmm(passed), hhmm(self.active_session().duration))
            line4 = 'rem: {}'.format(humanize.naturaldelta(remaining))
        else:
            line1 = '-/-: No sessions.'
            line3 = 'dur: --.--/--.--'
            line4 = '     Completed.'
        self.lcddc().message( [ line1, line2, line3, line4 ], KnustService.Interval + 2)

    def _sigterm_handler(self):
        self.log().info('Received SIGTERM, terminating...')
        self._loop.quit()

    @classmethod
    def run(cls, configuration, hardware, sessionbus):
        loop = GLib.MainLoop()
        service = KnustService(loop, hardware, data_file_name="knust_sessions.json")
        service.maybe_reactivate_session()
        service.publish(sessionbus)
        GObject.timeout_add_seconds(KnustService.Interval, service._session_tick)
        GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, service._sigterm_handler)
        loop.run()
