#! /usr/bin/env python

__author__ = 'Dmitry'

import ownet
import paho.mqtt.client as mqtt
import time
import sys


class FrontDoor:
    def __init__(self):
        self._mqttc = mqtt.Client("front door")
        self._mqttc.on_message = self.mqtt_on_message
        self._working = 0

    def _getLockPos(self, byte, shift):
        if not (byte & (1 << (shift + 2))):
            return 3
        elif not (byte & (1 << (shift + 1))):
            return 2
        elif not (byte & (1 << (shift + 0))):
            return 1
        else:
            return 0

    def mqtt_on_message(self, mqttc, obj, msg):

        if msg.topic.startswith('home'):
            print msg.topic, msg.payload
            return

        if self._working:
            return

        self._working = 1
#        print(msg.topic)

        sensed = self._ctl.sensed_BYTE
        self._ctl.latch_0 = 1

        v = self._getLockPos(sensed, 0)
        self._mqttc.publish("home/front door/locks/upper", v, 2, True)

        v = self._getLockPos(sensed, 3)
        self._mqttc.publish("home/front door/locks/lower", v, 2, True)

        v = 'open' if sensed & (1 << 6) else 'closed'
        self._mqttc.publish("home/front door/door", v, 2, True)

        v = 'released' if sensed & (1 << 7) else 'pressed'
        self._mqttc.publish("home/front door/button", v, 2, True)

        self._working = 0

    def run(self):
        ownet.init('server:4304')
        self._ctl = ownet.Sensor('/Ctl_FrontDoor')
        self._ctl.out_of_testmode = 1
        self._ctl.por = 0
        self._ctl.latch_0 = 1
        self._ctl.set_alarm = "133333333"

        self._mqttc.connect("server", 1883, 60)
        self._mqttc.subscribe("buses/1w/alarm/Ctl_FrontDoor", 0)
        self._mqttc.subscribe("home/front door/#", 0)

        rc = 0
        while rc == 0:
            rc = self._mqttc.loop()

        ownet.finish()
        return rc

door = FrontDoor()
rc = door.run()
print("rc: "+str(rc))




def getLockPos(byte, shift):
    if not (byte & (1 << (shift + 2))):
        return '3'
    elif not (byte & (1 << (shift + 1))):
        return '2'
    elif not (byte & (1 << (shift + 0))):
        return '1'
    else:
        return 'open'


ownet.init('server:4304')
sensor = ownet.Sensor('/Ctl_FrontDoor')

sensor.PIO_BYTE = 0

#while 1:
#    for i in range(0, 6):
#        sensor.PIO_BYTE = (1 << i)

s = sensor.sensed_BYTE
while 1:
    snew = sensor.sensed_BYTE
    if snew != s:
        sd = s ^ snew

        localtime = time.localtime()
        timeString = time.strftime("%Y-%m-%d %H:%M:%S", localtime)

        wassup = ''

        if sd & (7 << 0):
            if wassup != '':
                wassup += ', '
            wassup += ' upper '
            wassup += getLockPos(s, 0) + ' -> ' + getLockPos(snew, 0)

        if sd & (7 << 3):
            if wassup != '':
                wassup += ', '
            wassup += ' lower '
            wassup += getLockPos(s, 3) + ' -> ' + getLockPos(snew, 3)

        if sd & (1 << 6):
            if wassup != '':
                wassup += ', '
            wassup += ' door '
            if snew & (1 << 6):
                wassup += 'open'
            else:
                wassup += 'closed'

        if sd & (1 << 7):
            if wassup != '':
                wassup += ', '
            wassup += ' button '
            if snew & (1 << 7):
                wassup += 'released'
            else:
                wassup += 'pressed'

        s = snew

        print timeString, wassup
        sys.stdout.flush()

ownet.finish()
