#! /usr/bin/env python3

import os
import json
import time
import argparse

import db.redisdb as redisdb
import core.logger as log
import core.config as config

# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for scheduler')
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")
arg_parser.add_argument('-m', '--mappingfile', help="Optional - Mapping file path")
args = vars(arg_parser.parse_args())

# Validate input - Log file
if args['logfile'] is not None:
    logfilepath = args['logfile']
else:
    logfilepath = config.content.logging['path']

# Setup logging
logfile = log.CreateLogger(toconsole=False,
                           tofile=True,
                           filepath=logfilepath,
                           level=config.content.logging['level'])

assert logfile, "Failed to create log outputs"


# Validate input - Mapping file
if args['mappingfile'] is not None:
    gpio_mapping_filepath = args['mappingfile']
else:
    local_path = os.path.dirname(os.path.abspath(__file__))
    gpio_mapping_filepath = local_path + config.DEFAULT_MAPPING_FILE

assert os.path.isfile(gpio_mapping_filepath), "GPIO mapping file not found"

## Open mapping file
with open(gpio_mapping_filepath) as gpio_mapping_file:
    gpio_mapping = json.load(gpio_mapping_file)
    logfile.info("loading GPIO mapping file %r" % gpio_mapping_filepath)



# Set all relays to off initially
db_relay_entries = redisdb.getObjects()
for entry in db_relay_entries:
    redisdb.setObject(entry, "off")


while True:
    for mapping in gpio_mapping['mapping']:
        relay = mapping
        gpio_pin = gpio_mapping['mapping'][mapping]
        gpio_state = redisdb.getObject(relay)

        if gpio_state == "on":
            logfile.info("turning on pin " + gpio_pin)
        else:
            logfile.info("turning off pin " + gpio_pin)

    time.sleep(2)