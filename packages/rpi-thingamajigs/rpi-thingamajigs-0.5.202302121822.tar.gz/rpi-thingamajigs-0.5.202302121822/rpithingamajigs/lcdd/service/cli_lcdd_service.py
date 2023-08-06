import click
import yaml
import logging
import logging.config
import os
from rpithingamajigs.lcdd.service.lcdd import LCDD
from rpithingamajigs.lcdd.service.configuration import Configuration

@click.command()
@click.option('--config', '-c', required=False, type=click.Path(dir_okay=False), default='/etc/lcdd/config.yaml', help='The LCDD configuration file.')
@click.option('--logconfig', '-l', required=False, type=click.Path(dir_okay=False), default='/etc/lcdd/log-config.yaml', help='The LCDD logging configuration file.')
@click.option('--sessionbus/--no-sessionbus', '-s', required=False, default=False, help='Use the DBUS session bus instead of the system bus.')
def lcdd(config, logconfig, sessionbus):
    """LCDD implements a DBUS service to manage messages to an LCD display."""
    with open(logconfig, 'rb') as logconfig_file:
        logconfiguration = yaml.safe_load(logconfig_file)
        logging.config.dictConfig(logconfiguration)
    logging.info("configuration: {}".format(config))
    logging.info("logging configuration: {}".format(logconfig))
    logging.debug("working directory: {}".format(os.getcwd()))
    try:
        configuration = Configuration.initialize(config, sessionbus)
        LCDD(configuration).run()
    except Exception as e:
        logging.error('Terminating: {}'.format(str(e)))
        raise click.Abort(str(e))
if __name__ == '__main__':
    lcdd()  # pylint: disable=no-value-for-parameter
