#! /usr/bin/env python3

import os
import argparse
import datetime

from functools import wraps

from bottle import get, post, route, run, template, request, static_file, redirect, Bottle, response
import bottle_redis

import core.config as config
import core.logger as log

# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for http server')
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")
args = vars(arg_parser.parse_args())

# Validate input - Log file
if args['logfile'] is not None:
    logfilepath = args['logfile']
else:
    logfilepath = config.content.httplogging['path']

# Setup logging
logfile = log.CreateLogger(toconsole=False,
                           tofile=True,
                           filepath=logfilepath,
                           level=config.content.httplogging['level'])

assert logfile, "Failed to create log outputs"

def log_to_logger(fn):
    '''
    Wrap a Bottle request so that a log line is emitted after it's handled.
    (This decorator can be extended to take the desired logger as a param.)
    '''
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.datetime.now()
        actual_response = fn(*args, **kwargs)
        # modify this to log exactly what you need:
        logfile.info('%s %s %s %s %s' % (request.remote_addr,
                                        request_time,
                                        request.method,
                                        request.url,
                                        response.status))
        return actual_response
    return _log_to_logger


app = Bottle()
plugin = bottle_redis.RedisPlugin(host='localhost')
app.install(plugin)
app.install(log_to_logger)

@app.route('/')
def form():
   return template("templates/main.tpl", page_title="Pi Controls")


@app.route('/page_relay.html')
def page_relay(rdb):
    relay_1_state = rdb.get('relay_1').decode('utf-8')
    relay_2_state = rdb.get("relay_2").decode('utf-8')
    relay_3_state = rdb.get("relay_3").decode('utf-8')
    relay_4_state = rdb.get("relay_4").decode('utf-8')

    if relay_1_state == "off":
        relay_1_off = "checked"
        relay_1_on = ""
    else:
        relay_1_on = "checked"
        relay_1_off = ""

    if relay_2_state == "off":
        relay_2_off = "checked"
        relay_2_on = ""
    else:
        relay_2_on = "checked"
        relay_2_off = ""

    if relay_3_state == "off":
        relay_3_off = "checked"
        relay_3_on = ""
    else:
        relay_3_on = "checked"
        relay_3_off = ""

    if relay_4_state == "off":
        relay_4_off = "checked"
        relay_4_on = ""
    else:
        relay_4_on = "checked"
        relay_4_off = ""

    return template('./templates/page_relay.tpl',
                    relay_1_on=relay_1_on, relay_1_off=relay_1_off,
                    relay_2_on=relay_2_on, relay_2_off=relay_2_off,
                    relay_3_on=relay_3_on, relay_3_off=relay_3_off,
                    relay_4_on=relay_4_on, relay_4_off=relay_4_off,
                    page_title="Pi Controls - Relays")

@app.route('/page_sensor.html')
def page_sensor(rdb):
    return static_file("landing.html", root='./pages')

@app.route('/page_system.html')
def page_system(rdb):
    return static_file("landing.html", root='./pages')


@app.route('/<filename>')
def files(filename):
    name, ext = os.path.splitext(filename)
    if ext == ".html":
        return static_file(filename, root='./pages')
    elif ext == ".css":
        return static_file(filename, root='./style')


@app.route('/images/<filename>')
def files(filename):
    return static_file(filename, root='./images')


@app.post('/relayinput')
def submit(rdb):
    relay = int(request.forms.get('relay'))
    source_page = request.forms.get('page')
    relay_state = request.forms.get('state')

    rdb.set("relay_" + str(relay), relay_state)

    redirect(source_page)


app.run(host=config.content.httpserver['ip_address'], port=int(config.content.httpserver['port']), quiet=True)