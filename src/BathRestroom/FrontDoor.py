#! /usr/bin/env python

__author__ = 'Dmitry'

import ownet
import time
import sys


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

#while 1:
#    #sensor.PIO_BYTE = (1 << 7)
#    sensor.PIO_BYTE = 0
#
#while 1:
#    for i in range(0, 6):
#        sensor.PIO_BYTE = (1 << i)

s = 0
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
