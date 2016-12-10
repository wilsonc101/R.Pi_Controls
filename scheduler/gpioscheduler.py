#! /usr/bin/env python3

import json
import time

import RPi.GPIO as gpio

import core.redisdb as redisdb
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
        db_relay_entries = redisdb.getObjects(key="relay_[0-9]")

        for entry in db_relay_entries:
            redisdb.setObject(entry, config.content.relay_defaults[entry])
            self.logfile.info("Setting default - turning " + config.content.relay_defaults[entry] + " " + entry)


    def run_schedule(self):
        current_state = dict()

        while True:
            now_hour = int(time.strftime("%H"))
            now_min = int(time.strftime("%M"))

            for mapping in self.gpio_mapping['mapping']:
                relay = mapping

                # Convert on/off times to Redis state
                gpio_on_hour, gpio_on_min = redisdb.getObject(relay + "_on").split(":")
                gpio_off_hour, gpio_off_min = redisdb.getObject(relay + "_off").split(":")

                # Set state to ON
                if int(gpio_on_hour) == now_hour and int(gpio_on_min) == now_min:
                    self.logfile.info("scheduled switch on for " + relay)
                    redisdb.setObject(relay, "on")

                # Set state to OFF
                if int(gpio_off_hour) == now_hour and int(gpio_off_min) == now_min:
                    self.logfile.info("scheduled switch off for " + relay)
                    redisdb.setObject(relay, "off")


                # Convert Redis state to GPIO
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
