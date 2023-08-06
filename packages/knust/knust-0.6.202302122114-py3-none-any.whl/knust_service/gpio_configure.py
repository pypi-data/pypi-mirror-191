# Reset the GPIO pins. This is usually performed on startup of the application.
import logging
import Adafruit_DHT
import RPi.GPIO as GPIO

class GpioConfigurator():
    def __init__(self, configuration):
        assert configuration != None
        self._configuration = configuration

    def configure(self):
        """Configure all sensor pins as IN and all relais pins as OUT."""
        logging.info('Setting up GPIO pin configuration...')
        GPIO.setmode(GPIO.BCM)

        sensors = self._configuration.sensors()
        for name, sensor in sensors.items():
            pin = self._configuration.gpiopin(name, sensor)
            # not all sensors have GPIO pins...
            if not pin:
                logging.info('No GPIO pin configured for sensor {}.'.format(name))
                continue
            logging.info('Configuring GPIO pin {} for sensor {} as input.'.format(pin, name))
            GPIO.setup(pin, GPIO.IN)

        relaises = self._configuration.relais()
        for name, relais in relaises.items():
            pin = self._configuration.gpiopin(name, relais)
            if not pin:
                raise RuntimeError('GPIO pin is required, but not configured for relais {}.'.format(name))
            logging.info('Configuring GPIO pin {} for relais {} as output.'.format(pin, name))
            GPIO.setup(pin, GPIO.OUT)
            # ... turn relais off by default:
            GPIO.output(pin, GPIO.HIGH)

    def cleanup(self):
        logging.info('Cleaning up GPIO pin configuration...')
        GPIO.cleanup()
