# The HardwareRaspberry class.
from knust_service.hardware_interface import HardwareInterface
from knust_service.gpio_configure import GpioConfigurator
import RPi.GPIO as GPIO
from rpithingamajigs.temperature_sensor.dht22_reader import DHT22Reader

class HardwareRaspberry(HardwareInterface):
    def __init__(self, configuration):
        super().__init__(configuration)
        self._gpio_configurator = GpioConfigurator(self.configuration)
        self._temperature_reader = None
        self._relais = None

    @property
    def temperature_reader(self):
        return self._temperature_reader

    @temperature_reader.setter
    def temperature_reader(self, value):
        self._temperature_reader = value

    @property
    def relais(self):
        return self._relais

    @relais.setter
    def relais(self, value):
        self._relais = value

    def setup(self):
        self.log().info('Setting up Raspberry Pi hardware.')
        self._gpio_configurator.configure()
        device = self.configuration.device()
        if not device:
            raise RuntimeError('No Knust device configured.')
        self.log().info('Setting up Knust device named "{}".'.format(device['name']))
        sensor_name = device.get('sensor')
        sensor = self.configuration.get_sensor(sensor_name)
        assert sensor is not None # configuration.device() performs a sanity check
        sensor_type = sensor.get('type', None)
        if sensor_type != 'dht22':
            raise RuntimeError('Unsupported sensor type {}.'.format(sensor_type))
        self.log().info('Setting up temperature sensor {} for sensor {}.'.format(sensor_type, sensor_name))
        gpiopin = self.configuration.gpiopin(sensor_name, sensor)
        self.temperature_reader = DHT22Reader(gpiopin, self.temperature_sensor)
        self.temperature_reader.start()
        self.log().debug('Temperature reader started.')
        relais_name = device.get('relais')
        self.relais = self.configuration.get_relais(relais_name)
        self.relais['name'] = relais_name

    def teardown(self):
        self.log().info('Tearing down Raspberry Pi hardware.')
        if self.temperature_reader:
            self.log().debug('Terminating temperature sensor reader...')
            self.temperature_reader.quit()
            self.temperature_reader.join()
        self.set_heater_on(False)
        self.log().debug('Cleaning up GPIO pin configuration...')
        self._gpio_configurator.cleanup()

    def is_ready(self):
        return self.configuration is not None

    def describe(self):
        return 'Raspberry Pi hardware implementation'

    def set_heater_on(self, onOff):
        status = 'ON' if onOff else 'OFF'
        if not self.relais:
            self.log().warning('Asked to set heater to {}, but no relais configured.'.format(status))
        gpiopin = self.configuration.gpiopin(self.relais.get('name'), self.relais)
        GPIO.output(gpiopin, GPIO.LOW if onOff else GPIO.HIGH)
        self.log().debug('Heater set to {}.'.format(status))
        return True
