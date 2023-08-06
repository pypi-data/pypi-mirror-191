# The HardwareSimulator class.
import logging
from knust_service.hardware_interface import HardwareInterface

class HardwareSimulator(HardwareInterface):
    def __init__(self, configuration):
        super().__init__(configuration)

    def setup(self):
        self.log().debug('Setting up simulated hardware.')

    def teardown(self):
        self.log().debug('Tearing down simulated hardware.')

    def is_ready(self):
        return self.configuration is not None

    def describe(self):
        return 'hardware simulator for testing'

    def set_heater_on(self, onOff):
        if onOff:
            self.log().debug('Set heater to ON...')
        else:
            self.log().debug('Set heater to OFF...')
        return True
