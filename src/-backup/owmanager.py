#! /usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import pyownet.protocol as onewire
import time
from time import sleep
from Temperatures import Temperatures
from FrontDoor import FrontDoor
from BathRestRoom import BathRestRoom

class OWManager:

    def __init__(self, ow):
        self._ow = ow

        #self._plugins = {'Ctl_FrontDoor': FrontDoor(), 'Ctl_BR': BathroomRestroom()}
        #self._mqttc = mqtt.Client("ow manager")
        #self._mqttc.on_message = self.mqtt_on_message
        #self._path = '/alarm'

    def mqtt_on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def run(self):
        i = 0
        while 1:
            i = (i + 1) % 3
            #d = self._ow.dir('/alarm')
            #print i, 'dir'
            print i, self._ow.read('/Ctl_FrontDoor/sensed.ALL')
            #time.sleep(0.01)
            yield


        #t = Temperatures()
        #while 1:
        #    t.refresh()
        #    sleep(3)


        #self._mqttc.connect("server", 1883, 60)
        #self._mqttc.subscribe("buses/1w/#", 2)

        #rc = 0
        #while rc == 0:
        #    rc = self._mqttc.loop(0.01)
        #    for e in self._alarm.entries():
        #        self._mqttc.publish("buses/1w/alarm/" + e, None, 0, False)

        #return rc

import Queue


def scheduler(tasks):
    queue = Queue.Queue()
    for task in tasks:
        queue.put(task())

    while not queue.empty():
        task = queue.get()
        try:
            next(task)
            queue.put(task)
        except StopIteration:
            pass


ow = onewire.OwnetProxy(host='server', port=4304)

manager = OWManager(ow)
front_door = FrontDoor(ow)
bath_rest_room = BathRestRoom(ow)
temperatures = Temperatures(ow, {
    'Temp_Bathroom': 'Ванная',
    'Temp_Kitchen': 'Кухня',
    'Temp_Living': 'Гостиная',
    'Temp_Bedroom': 'Спальня',
    'Temp_Kids': 'Детская',
    'Temp_Closet': 'Кладовая',
})

scheduler([
    #manager.run,
    front_door.run,
    bath_rest_room.run,
    temperatures.run,
])
