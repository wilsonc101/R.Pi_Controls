#! /usr/bin/env python3

import datetime
import os
import time

from functools import wraps
from bottle import get, post, route, run, template, request, static_file, redirect, Bottle, response
import bottle_redis

import core.config as config
import core.sensors as sensors

DEFAULT_RELAY_STATE = config.content.relay_defaults


class WebServer():
    app = Bottle()

    def __init__(self, logfile):
        plugin = bottle_redis.RedisPlugin(host=config.content.redis['server'])
        self.app.install(plugin)
        self.app.install(self.log_to_logger)
        self.logfile = logfile

    def log_to_logger(self, fn):
        '''
        Wrap a Bottle request so that a log line is emitted after it's handled.
        (This decorator can be extended to take the desired logger as a param.)
        '''
        @wraps(fn)
        def _log_to_logger( *args, **kwargs):
            request_time = datetime.datetime.now()
            actual_response = fn(self, **kwargs)
            # modify this to log exactly what you need:
            self.logfile.info('%s %s %s %s %s' % (request.remote_addr,
                                            request_time,
                                            request.method,
                                            request.url,
                                            response.status))
            return actual_response
        return _log_to_logger

    @app.route('/')
    def form(self):
       current_time = time.strftime("%a, %d %b %Y  -  %H:%M:%S")
       return template("webserver/templates/main.tpl", page_title="Pi Controls", now=current_time)

    @app.route('/page_relay.html')
    def page_relay(self, rdb):

        relay_state = DEFAULT_RELAY_STATE

        relay_data = dict()

        for relay in relay_state.keys():
            relay_data[relay] = rdb.get(relay).decode('utf-8')

            on_hour, on_min = rdb.get(relay + "_on").decode('utf-8').split(":")
            off_hour, off_min = rdb.get(relay + "_off").decode('utf-8').split(":")

            relay_data[relay + "_on_hour"] = int(on_hour)
            relay_data[relay + "_on_min"] = int(on_min)

            relay_data[relay + "_off_hour"] = int(off_hour)
            relay_data[relay + "_off_min"] = int(off_min)

        return template('./webserver/templates/page_relay.tpl',
                        page_title="Pi Controls - Relays",
                        **relay_data)

    @app.route('/page_sensor.html')
    def page_sensor(self, rdb):
        sensor_data = sensors.get_sensor_data()

        return template('./webserver/templates/page_sensor.tpl',
                        page_title="Pi Controls - Sensors",
                        **sensor_data)

    @app.route('/page_system.html')
    def page_system(self, rdb):
        return static_file("landing.html", root='./webserver/pages')

    @app.route('/<filename>')
    def files(self, filename):
        name, ext = os.path.splitext(filename)
        if ext == ".html":
            return static_file(filename, root='./webserver/pages')
        elif ext == ".css":
            return static_file(filename, root='./webserver/style')
        elif ext == ".js":
            return static_file(filename, root='./webserver/scripts')

    @app.route('/images/<filename>')
    def files(self, filename):
        return static_file(filename, root='./webserver/images')

    @app.post('/relayinput')
    def submit(self, rdb):
        source_page = request.forms.get('page')

        for relay_id in range(1, 5):
            relay_state = request.forms.get('state_' + str(relay_id))
            rdb.set("relay_" + str(relay_id), relay_state)

        redirect(source_page)

    @app.post('/scheduleinput')
    def submit(self, rdb):
        source_page = request.forms.get('page')

        for relay_id in range(1, 5):
            on_hour = str(request.forms.get('on_hour_' + str(relay_id)))
            on_min = str(request.forms.get('on_min_' + str(relay_id)))

            off_hour = str(request.forms.get('off_hour_' + str(relay_id)))
            off_min = str(request.forms.get('off_min_' + str(relay_id)))

            rdb.set("relay_" + str(relay_id) + "_on", on_hour + ":" + on_min)
            rdb.set("relay_" + str(relay_id) + "_off", off_hour + ":" + off_min)

        redirect(source_page)


    def run_server(self):
        self.app.run(host=config.content.httpserver['ip_address'],
                     port=int(config.content.httpserver['port']),
                     quiet=True)

