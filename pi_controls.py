#! /usr/bin/env python3

import argparse
import os
import json
import multiprocessing
import time

import core.config as config
import core.logger as log
import core.redisdb as redisdb

from webserver import server
from scheduler import gpioscheduler, sensormonitor


# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Pi Controls options')
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")
arg_parser.add_argument('-m', '--mappingfile', help="Optional - GPIO Mapping file path for scheduler")
arg_parser.add_argument('--firstrun', dest='firstrun', action='store_true', help="Optional - Create Redis objects")
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
    local_path = os.path.abspath(os.path.join(os.path.abspath(__file__), ".."))
    gpio_mapping_filepath = local_path + config.DEFAULT_MAPPING_FILE

assert os.path.isfile(gpio_mapping_filepath), "GPIO mapping file not found"

# Create Redis objects on first run
if args['firstrun']:
    with open(gpio_mapping_filepath) as mappingfile:
        # Create relay records
        mapping_keys = [i for i in json.load(mappingfile)['mapping'].keys()]
        for key in mapping_keys:
            redisdb.createObject(key, "off")
            redisdb.createObject(key + "_on", "00:00")
            redisdb.createObject(key + "_off", "00:00")

        # Create sensor records
        sensor_keys = [i for i in json.load(mappingfile)['sensors'].keys()]
        for key in mapping_keys:
            redisdb.createObject(key, "0")


if not args['runwebserver'] and not args['runscheduler']:
    # Setup scheduler thread
    print("Starting PiControl Scheduler....")
    # GPIO
    gpio_scheduler = gpioscheduler.ControlScheduler(logfile, gpio_mapping_filepath)
    scheduler_worker = multiprocessing.Process(target=gpio_scheduler.run_schedule)
    scheduler_worker.daemon = True
    scheduler_worker.start()

    # Sensors
    sensor_monitor = sensormonitor.SensorMonitor(logfile)
    monitor_worker = multiprocessing.Process(target=sensor_monitor.run_schedule)
    monitor_worker.daemon = True
    monitor_worker.start()
    print("....done.")

    # Start webserver thread
    print("Starting PiControl Webserver....")
    pi_controls_webserver = server.WebServer(logfile)
    webserver_worker = multiprocessing.Process(target=pi_controls_webserver.run_server)
    webserver_worker.daemon = True
    webserver_worker.start()
    print("....done.")

while True:
    time.sleep(1)
