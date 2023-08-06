# The knust_service. It runs as a daemon and prepares your knust.

import click
import os
import yaml
import logging
import logging.config
from knust_service.configuration import Configuration
from knust_service.hardware_factory import hardware_factory
from knust_service.service import KnustService

@click.command()
@click.option('--config', '-c', required=False, type=click.File('rb'), default='/etc/knust/config.yaml', help='The Knust configuration file.')
@click.option('--logconfig', '-l', required=False, type=click.File('rb'), default='/etc/knust/log-config.yaml', help='The Knust logging configuration file.')
@click.option('--sessionbus/--no-sessionbus', '-s', required=False, default=False, help='Use the DBUS session bus instead of the system bus.')
def knust_service(config, logconfig, sessionbus):
    logconfiguration = yaml.safe_load(logconfig.read())
    logging.config.dictConfig(logconfiguration)
    logging.info("configuration: {}".format(config.name))
    logging.info("logging configuration: {}".format(logconfig.name))
    logging.debug("working directory: {}".format(os.getcwd()))
    configuration = Configuration()
    configuration.load_from_buffer(config)
    try:
        with hardware_factory(configuration) as hardware:
            logging.info('Set up {}.'.format(hardware.describe()))
            KnustService.run(configuration, hardware, sessionbus)
    except Exception as e:
        logging.error('Terminating: {}'.format(str(e)))
        raise click.Abort(str(e))

if __name__ == '__main__':
    knust_service()  # pylint: disable=no-value-for-parameter
