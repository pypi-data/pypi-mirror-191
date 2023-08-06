# Read the static Knust configuration from the config file.
import yaml
import logging

class Configuration():
    """Configuration loads configuration data and presents it to the application."""
    def __init__(self, location="/etc/knust/config.yaml"):
        self._location = location
        self._config = None

    @property
    def location(self):
        """The location of the configuration file."""
        return self._location

    @location.setter
    def location(self, value):
        """Set the location of the configuration file."""
        self._location = value

    @property
    def data(self):
        """Data returns either an empty YAML document or the one set by load()."""
        return self._config or {}

    def sensors(self):
        """Return all configured sensors."""
        return self.data.get('sensors', {})

    def get_sensor(self, name):
        """Get a sensor configuration by name."""
        sensors = self.sensors()
        if not sensors:
            return None
        return sensors.get(name, None)

    def relais(self):
        """Return all configured relais."""
        return self.data.get('relais', {})

    def get_relais(self, name):
        """Get a relais configuration by name."""
        relaises = self.relais()
        if not relaises:
            return None
        return relaises.get(name, None)

    def device(self):
        """Currently only one device configuration is supported.
        If more than one are read, the first one will be used."""
        devices = self.data.get('devices', {})
        if devices:
            first = next(iter(devices))
            device = devices[first]
            # sanity check
            sensor = device.get('sensor') or ''
            if not sensor:
                raise RuntimeError('No sensor name configured for device {}.'.format(first))
            if not self.get_sensor(sensor):
                raise RuntimeError('Unknown sensor name {} configured for device {}.'.format(sensor, first))
            relais = device.get('relais') or ''
            if not relais:
                raise RuntimeError('No relais name configured for device {}.'.format(first))
            if not self.get_relais(relais):
                raise RuntimeError('Unknown relais name {} configured for device {}.'.format(relais, first))
            device['name'] = first
            return device
        else:
            return {}

    def load(self):
        """Load the configuation file, passing all errors on to the caller."""
        with open(self.location, "r") as configfile:
            self.load_from_buffer(configfile)

    def load_from_buffer(self, buffer):
        """Load the configuration directly from the specified buffer, expexted to be ready for reading."""
        self._config = yaml.load(buffer, Loader=yaml.BaseLoader)

    # TODO the use of name is weird...
    def gpiopin(self, name, interface):
        """Return the configured GPIO pin for a defined interface (sensor or relais) as an integer, or None. Raise an error if the value is not a number."""
        pin = interface.get('gpiopin', None)
        if not pin:
            return None
        try:
            pin_number = int(pin)
            if pin_number < 2 or pin_number > 26:
                raise ValueError('Raspberry Pi GPIO pin numbers must be between 2 and 26 (got {}).'.format(pin_number))
            return pin_number
        except ValueError as e:
            logging.error('Expected integer number for GPIO pin of interface {}, got {}.'.format(name, pin))
            raise e
