#! /usr/bin/env python3

import os
import json
import time

import core.redisdb as redisdb
import core.logger as log
import core.config as config



class ControlScheduler():
    def __init__(self, logfile, mappingfilepath):
        # Open mapping file
        with open(mappingfilepath) as gpio_mapping_file:
            self.gpio_mapping = json.load(gpio_mapping_file)
            logfile.info("loading GPIO mapping file %r" % gpio_mapping_filepath)

        # Set all relays to off initially
        db_relay_entries = redisdb.getObjects(key="relay*")
        for entry in db_relay_entries:
            redisdb.setObject(entry, "off")

    def run_schedule(self):
        while True:
            for mapping in self.gpio_mapping['mapping']:
                relay = mapping
                # gpio_pin = gpio_mapping['mapping'][mapping]
                # gpio_state = redisdb.getObject(relay)

                # if gpio_state == "on":
                #    logfile.info("turning on pin " + gpio_pin)
                # else:
                #    logfile.info("turning off pin " + gpio_pin)

            time.sleep(2)



