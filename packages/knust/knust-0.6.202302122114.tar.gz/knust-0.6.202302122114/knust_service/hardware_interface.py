# The HardwareInterface class.
import logging
from rpithingamajigs.temperature_sensor import TemperatureSensor, Measurement

class HardwareInterface:
    '''HardwareInterface defines the methods provided to interface with peripherals.'''
    def __init__(self, configuration):
        self._configuration = configuration
        self._log = logging.getLogger('hardware')
        self.temperature_sensor = TemperatureSensor()

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, value):
        self._configuration = value

    @property
    def temperature_sensor(self):
        return self._temperature_sensor

    @temperature_sensor.setter
    def temperature_sensor(self, value):
        assert value is None or isinstance(value, TemperatureSensor)
        self._temperature_sensor = value


    def log(self):
        return self._log

    def describe(self):
        raise NotImplementedError('Abstract base class method called.')

    def setup(self):
        raise NotImplementedError('Abstract base class method called.')

    def teardown(self):
        raise NotImplementedError('Abstract base class method called.')

    def is_ready(self):
        raise NotImplementedError('Abstract base class method called.')

    def set_heater_on(self, onOff):
        raise NotImplementedError('Abstract base class method called.')
