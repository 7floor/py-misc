#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
        self._upper = True
        self._lower = True

    def mqtt_on_message(self, mqttc, obj, msg):
        if msg.topic == "home/front door/lock/upper":
            self._upper = False if msg.payload == "0" else True
        if msg.topic == "home/front door/lock/lower":
            self._lower = False if msg.payload == "0" else True

    def _sleep(self, sec):
        t = time.time()
        while time.time() - t < sec:
            self._mqttc.loop(0.1)

    def _locked(self):
        return self._upper or self._lower

    def _set_alarm(self, on):
        self._mqttc.publish("home/front door/alarm", ("LS" if on else ""), 2, False)
        self._mqttc.loop(0)

    def run(self):
        while True:
            print "locked"
            self._set_alarm(False)
            while self._locked():
                self._sleep(0.1)

            print "unlocked, will alarm soon"
            timeout = 60  # allow 60 seconds for unlocked door
            t = time.time()
            while time.time() - t < timeout and not self._locked():
                self._sleep(1)

            if self._locked():
                continue

            print "alarming"
            self._set_alarm(True)

            while not self._locked():
                self._sleep(0.1)


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
print 'Started'

fdg = FdGuard()
fdg.run()