#! /usr/bin/env python3

import os
import json
import time

import RPi.GPIO as gpio

import core.redisdb as redisdb
import core.logger as log
import core.config as config


class ControlScheduler():
    def __init__(self, logfile, mappingfilepath):
        self.logfile = logfile

        # Open mapping file
        with open(mappingfilepath) as gpio_mapping_file:
            self.gpio_mapping = json.load(gpio_mapping_file)
            logfile.info("loading GPIO mapping file %r" % mappingfilepath)

        # Set outputs in default state
        self.initilise_outputs()
        self.initilise_gpio()


    def initilise_gpio(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        for mapping in self.gpio_mapping['mapping']:
            gpio_pin = int(self.gpio_mapping['mapping'][mapping])
            gpio.setup(gpio_pin, gpio.OUT)


    def initilise_outputs(self):
        # Set all relays to default state
        db_relay_entries = redisdb.getObjects(key="relay*")

        for entry in db_relay_entries:
            redisdb.setObject(entry, config.content.relay_defaults[entry])
            self.logfile.info("Setting default - turning " + config.content.relay_defaults[entry] + " " + entry)


    def run_schedule(self):
        current_state = dict()

        while True:
            for mapping in self.gpio_mapping['mapping']:
                relay = mapping
                gpio_pin = int(self.gpio_mapping['mapping'][mapping])
                gpio_state = redisdb.getObject(relay)
                            
                # Populate current state dict
                if gpio_pin not in current_state:
                    current_state[gpio_pin] = None
                
                # Check if something has changed since last loop
                if current_state[gpio_pin] != gpio_state:
                     current_state[gpio_pin] = gpio_state

                     if gpio_state == "on":
                        self.logfile.info("turning on pin " + str(gpio_pin))
                        gpio.output(gpio_pin, True)

                     else:
                        self.logfile.info("turning off pin " + str(gpio_pin))
                        gpio.output(gpio_pin, False)

            time.sleep(1)
