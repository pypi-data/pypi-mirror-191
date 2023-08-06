import logging
import os
import yaml
from rpithingamajigs.chardisplay import SimulatedConsoleDisplay

class Configuration():
    def __init__(self, configuration_dict, sessionbus):
        assert configuration_dict != None
        self._configuration_dict = configuration_dict
        self._sessionbus = sessionbus

    def display(self):
        value = self._configuration_dict.get('display')
        if not value:
            raise RuntimeError("No display configured.")
        name = value.get('name', None)
        if not name:
            raise RuntimeError("No name specified for display.")
        type = value.get('type', None)
        if not type:
            raise RuntimeError("No type specified for display {}.".format(name))
        # This implements a poor man's "factory":
        device = None
        if type == "console":
            device = SimulatedConsoleDisplay(name)
        elif type == "i2c_16_02":
            try:
                from rpithingamajigs.chardisplay.display_i2c import I2C1602Display
                device = I2C1602Display(name)
            except ImportError as e:
                logging.error('Unable to import the I2C1602 display driver. Please check dependencies!')
                raise e
        elif type == "i2c_20_04":
            try:
                from rpithingamajigs.chardisplay.display_i2c import I2C2004Display
                device = I2C2004Display(name)
            except ImportError as e:
                logging.error('Unable to import the I2C2004 display driver. Please check dependencies!')
                raise e
        # elif ...: # ... other display types
        else:
            raise RuntimeError("Unsupported display type {} specified for display {}.".format(type, name))
        device.configure(value)
        return device

    def _settings(self):
        value = self._configuration_dict.get('settings')
        if not value:
            return {}
        return value

    def minimum_timeout(self):
        value = int(self._settings().get('min_timeout', 2))
        return value

    def motd(self):
        value = self._settings().get('motd', None)
        return value

    def farewell(self):
        value = self._settings().get('farewell', None)
        return value

    def use_sessionbus(self):
        """If true, use the DBUS session bus, otherwise the service will connect to the system bus."""
        return self._sessionbus

    @classmethod
    def initialize(cls, config_file_path, use_sessionbus):
        if not config_file_path:
            raise RuntimeError("No configuration file specified.")
        elif not os.path.exists(config_file_path):
            raise RuntimeError("Configuration file {} does not exist. Continuing without it.".format(config_file_path))
        with open(config_file_path, "r") as configfile:
            config = Configuration(yaml.load(configfile, Loader=yaml.BaseLoader), use_sessionbus)
            return config
