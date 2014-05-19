#! /usr/bin/env python

__author__ = 'Dmitry'

import ownet
import time

ownet.init('server:4304')
sensor = ownet.Sensor('/Ctl_FrontDoor')
s = 0
while 1:
    snew = sensor.sensed_BYTE
    if snew != s:
        sd = s ^ snew
        s = snew

        localtime = time.localtime()
        timeString  = time.strftime("%Y-%m-%d %H:%M:%S", localtime)

        wassup = ''

        if sd & (7 << 0):
            if wassup != '':
                wassup += ', '
            wassup += ' upper '
            if not (s & (1 << 2)):
                wassup += '3'
            elif not (s & (1 << 1)):
                wassup += '2'
            elif not (s & (1 << 0)):
                wassup += '1'
            else:
                wassup += 'open'

        if sd & (7 << 3):
            if wassup != '':
                wassup += ', '
            wassup += ' lower '
            if not (s & (1 << 5)):
                wassup += '3'
            elif not (s & (1 << 4)):
                wassup += '2'
            elif not (s & (1 << 3)):
                wassup += '1'
            else:
                wassup += 'open'

        if sd & (1 << 6):
            if wassup != '':
                wassup += ', '
            wassup += ' door '
            if s & (1 << 6):
                wassup += 'open'
            else:
                wassup += 'closed'

        if sd & (1 << 7):
            if wassup != '':
                wassup += ', '
            wassup += ' button '
            if s & (1 << 7):
                wassup += 'released'
            else:
                wassup += 'pressed'

        print timeString, wassup

ownet.finish()
