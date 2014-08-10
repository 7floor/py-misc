#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
default: alarm(off)
waiting: alarm(L), start timer
alarming: alarm(LS)

default - locks open -> waiting
default - door closed -> waiting (to reset after button)

waiting - locks closed -> default
waiting - button pressed -> default
waiting - timeout -> alarming

alarming - locks closed -> default
alarming - button pressed -> default

"""

import os
import sys
import time
import paho.mqtt.client as mqtt


class FdGuard():

    def __init__(self):
        self._mqttc = mqtt.Client("fd guard")
        self._mqttc.connect("server", 1883, 60)
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.subscribe("home/front door/#", 2)
        self._upper = self._lower = self._lock = True
        self._wait_start = time.time()
        self._state = "default"  # default waiting alarming
        self._enter_state()

    def mqtt_on_message(self, mqttc, obj, msg):
        if msg.topic == "home/front door/lock/upper":
            self._upper = False if msg.payload == "0" else True
        if msg.topic == "home/front door/lock/lower":
            self._lower = False if msg.payload == "0" else True
        if (self._upper or self._lower) != self._lock:
            self._lock = self._upper or self._lower
            self._lock_changed()

        if msg.topic == "home/front door/door" and msg.payload == "closed" and not self._lock:  # check locks to avoid wrong logic at startup
            self._door_closed()

        if msg.topic == "home/front door/button" and msg.payload == "pressed":
            self._button_pressed()

    def _lock_changed(self):
        if self._lock:
            self._state = "default"
        elif self._state == "default":
            self._state = "waiting"
        else:
            return
        self._enter_state()

    def _door_closed(self):
        if self._state == "default":
            self._state = "waiting"
            self._enter_state()

    def _button_pressed(self):
        self._state = "default"
        self._enter_state()

    def _enter_state(self):
        print self._state
        if self._state == "default":
            self._set_alarm("")
        elif self._state == "waiting":
            self._wait_start = time.time()
            self._set_alarm("L")
        elif self._state == "alarming":
            self._set_alarm("LS")

    def _set_alarm(self, mode):
        self._mqttc.publish("home/front door/alarm", mode, 2, False)
        self._mqttc.loop(0)

    def run(self):
        timeout = 60
        while True:
            while self._state != "waiting":
                self._mqttc.loop(0.1)

            while self._state == "waiting" and time.time() - self._wait_start < timeout:
                self._mqttc.loop(0.1)

            if self._state == "waiting":
                self._state = "alarming"
                self._enter_state()


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
print 'Started'

fdg = FdGuard()
fdg.run()
