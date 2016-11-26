import os
import configparser

from core import DEFAULT_CONFIG_FILE, DEFAULT_MAPPING_FILE


class configuration(object):
    def __init__(self, config_data):
        for key in config_data.keys():
            setattr(self, key, config_data[key])

local_path = os.path.abspath(os.path.join(os.path.dirname(__file__),  ".."))

config_filepath = str(local_path) + DEFAULT_CONFIG_FILE
assert os.path.isfile(config_filepath), "Config file not found"


config = configparser.ConfigParser()
config.read(config_filepath)

config_data = dict()
config_data['local_path'] = local_path    # Add in so we know where we are when executed

for section in config.sections():
    config_data[section] = {}

    for cfg_item in config.items(section):
        config_data[section][cfg_item[0]] = cfg_item[1]


content = configuration(config_data)

