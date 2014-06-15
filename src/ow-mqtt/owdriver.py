#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from coos import *
import time
import pyownet.protocol as onewire

import owalarm
import brr
import fd
from temperatures import temperatures


def sleeper():
    """ Saves CPU utilization """
    while True:
        time.sleep(0.01)
        yield


ow = onewire.OwnetProxy(host='server', port=4304)
obrr = brr.Brr(ow)
ofd = fd.Fd(ow)
sched = Scheduler()

sched.new(sleeper())
sched.new(owalarm.checkalarm(ow))
sched.new(obrr.run())
sched.new(ofd.run())
sched.new(temperatures(ow, {
    'Temp_Bathroom': 'Ванная',
    'Temp_Kitchen': 'Кухня',
    'Temp_Living': 'Гостиная',
    'Temp_Bedroom': 'Спальня',
    'Temp_Kids': 'Детская',
    'Temp_Closet': 'Кладовая',
}))

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
print 'Started'

sched.mainloop()
