from contextlib import contextmanager
from rpithingamajigs.platform import is_this_a_pi
from knust_service.hardware_simulator import HardwareSimulator

@contextmanager
def hardware_factory(configuration):
    try:
        interface = HardwareSimulator(configuration)
        if is_this_a_pi():
            try:
                from knust_service.hardware_raspberry import HardwareRaspberry
            except ModuleNotFoundError as e:
                raise RuntimeError('Unable to import Raspberry Pi hardware implementation. Please check dependencies: {}'.format(e))
            interface = HardwareRaspberry(configuration)
        assert interface is not None
        interface.setup()
        yield interface
    finally:
        interface.teardown()
