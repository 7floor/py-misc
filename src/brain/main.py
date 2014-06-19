#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent.monkey import patch_all; patch_all()  # this also patches the mqtt!!
from functools import wraps
import sys, os, inspect, glob


def mqtt_worker():
    mqtt_client.connect("server", 1883, 60)
    mqtt_client.subscribe("home/#", 2)
    while True:
        mqtt_client.loop()  # requires gevent monkey patch
    mqtt_client.disconnect()


def run_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        gevent.spawn(f, *args, **kwargs)
    return wrapper


def add_callback_params(f):
    @wraps(f)
    def wrapper(client, data, message):
        f(message)
    return wrapper


def message_callback_add_patched(self, sub, callback):
    callback = add_callback_params(run_async(callback))
    if callback is None or sub is None:
        raise ValueError("sub and callback must both be defined.")
    self._callback_mutex.acquire()
    self.on_message_filtered.append((sub, callback))
    self._callback_mutex.release()


def publish_impl(topic, payload, qos=0, retain=False):
    mqtt_client.publish(topic, payload, qos, retain)


def initialize():
    import plugin

    import paho.mqtt.client as mqtt
    #monkey patch mqtt to allow multiple callbacks per filter pattern
    mqtt.Client.message_callback_add = message_callback_add_patched
    global mqtt_client
    mqtt_client = mqtt.Client("brain")
    plugin.publish = publish_impl

    import logging
    root = logging.getLogger()
    root.setLevel(logging.NOTSET)

    formatter = logging.Formatter('%(asctime)s %(name)s.%(module)s %(levelname)s: %(message)s')

    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setFormatter(formatter)
    root.addHandler(out_handler)

    file_handler = logging.FileHandler('brain.log')
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    plugin.logger = logging.getLogger('brain')


def get_functions(module, predicate):
    return inspect.getmembers(module, lambda x: inspect.isfunction(x) and inspect.getmodule(x) == module and predicate(x))


def run_plugins():
    #add plugins sub folder to the system path
    plugin_path = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())) + '/plugins')
    if plugin_path not in sys.path:
        sys.path.insert(0, plugin_path)
    #enumerate plugins
    plugin_names = [os.path.basename(f)[:-3] for f in glob.glob(plugin_path + '/*.py')]
    logger.info('found plugins: %s', ', '.join(plugin_names))

    #import them and run if they are runnable
    for plugin_name in plugin_names:
        logger.info('loading %s', plugin_name)
        module = __import__(plugin_name)
        functions = get_functions(module, lambda x: hasattr(x, 'message_patterns'))
        for function in [f[1] for f in functions]:
            for pattern in function.message_patterns:
                mqtt_client.message_callback_add(pattern, function)

        functions = get_functions(module, lambda x: hasattr(x, 'executable'))
        for function in [f[1] for f in functions]:
            gevent.spawn(function)


def run():
    run_plugins()
    gevent.joinall([
        gevent.spawn(mqtt_worker),
    ])


initialize()
from plugin import *  # re-import everything so it will be available without "plugin." prefix
run()
