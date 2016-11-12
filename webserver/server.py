#! /usr/bin/env python3

import datetime
import os

from functools import wraps
from bottle import get, post, route, run, template, request, static_file, redirect, Bottle, response
import bottle_redis

import core.config as config

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
       return template("webserver/templates/main.tpl", page_title="Pi Controls")

    @app.route('/page_relay.html')
    def page_relay(self, rdb):

        relay_state = DEFAULT_RELAY_STATE

        for relay in relay_state.keys():
            relay_state[relay] = rdb.get(relay).decode('utf-8')

        return template('./webserver/templates/page_relay.tpl',
                        page_title="Pi Controls - Relays",
                        **relay_state)

    @app.route('/page_sensor.html')
    def page_sensor(self, rdb):
        return static_file("landing.html", root='./webserver/pages')

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
            on_hour = request.forms.get('on_hour_' + str(relay_id))
            on_min = request.forms.get('on_min_' + str(relay_id))

            off_hour = request.forms.get('off_hour_' + str(relay_id))
            off_min = request.forms.get('off_min_' + str(relay_id))

            if relay_id == 1:
                print("1 on: " + str(on_hour) + ":" + str(on_min))
            #rdb.set("relay_" + str(relay_id), relay_state)

        redirect(source_page)


    def run_server(self):
        self.app.run(host=config.content.httpserver['ip_address'],
                     port=int(config.content.httpserver['port']),
                     quiet=True)

