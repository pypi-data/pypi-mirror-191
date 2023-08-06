# A session is a task for the Knust service with a start time, a duration and a target temperature.
import json
from enum import Enum

class Session():
    class Status(Enum):
        NEW=1
        STARTED=2
        COMPLETED=3
        DROPPED=4

    def __init__(self, start_time = None, duration = None, target_temperature = None):
        self.start_time = start_time
        self.duration = duration
        self.target_temperature = target_temperature
        self.status = Session.Status.NEW

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        assert value == None or value >= 0
        self._duration = value

    @property
    def target_temperature(self):
        return self._target_temperature

    @target_temperature.setter
    def target_temperature(self, value):
        assert value == None or value >= 0
        self._target_temperature = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        assert Session.Status(value)
        self._status = value

    def __eq__(self, other):
        return self.start_time == other.start_time and \
            self.duration == other.duration and \
            self.target_temperature == other.target_temperature and \
            self.status == other.status
