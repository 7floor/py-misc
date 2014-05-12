#! /usr/bin/env python

import sys
import ownet
import time
from time import sleep

class CtlBR:

    _sensor = None
    _state = None
    _latch = None
    _strb = 0

    def __init__(self):
        self._sensor = ownet.Sensor('/Ctl_BR')
        self._sensor.useCache(False)
        self._sensor.out_of_testmode = 1
        self._sensor.por = 0
        self._sensor.set_alarm = "133333333"
        self._strb = self._sensor.strobe
        self.refresh_state()
        self.relax()

    def __del__(self):
        self._sensor = None

    def relax(self):
        """
        relaxes outputs so that can be read freely later
        to be called after any write
        """
        if self._sensor.PIO_BYTE != 0:
            if self._strb == 1:
                self._strb = 0
                self._sensor.strobe = 0
                print 'strobe 0'
            self._sensor.PIO_BYTE = 0
            print 'relaxed'

    def _in(self):
        self.relax()
        return self._sensor.sensed_BYTE

    def _out(self, data):
        if self._strb == 0:
            self._strb = 1
            self._sensor.strobe = 1
            print 'strobe 1'
        self._sensor.PIO_BYTE = ~data & 0xff

    def _set_address(self, address):
        a = (address << 2) | 0x03
        self._out(a)

    def knock(self, times):
        d = self._in()
        for i in range(times):
            self._out(d)

    def write(self, address, data):
        if address != 0:
            self._set_address(address)
        self._out(data)

    def read(self, address):
        if address != 0:
            self._set_address(address)
        d = self._in()
        if address != 0:
            self._out(d)
        return d

    def refresh_state(self):
        self._latch = self._sensor.latch_BYTE
        self._sensor.latch_0 = 1 #reset alarm by resetting latches
        self._state = ~self.read(0) & 0xff

    def send_state(self):
        self.write(0, ~self._state & 0xfc)

    def get_br_leak(self):
        return bool(self._state & (1 << 0))

    def get_rr_leak(self):
        return bool(self._state & (1 << 1))

    def get_br_light(self):
        return bool(self._state & (1 << 2))

    def set_br_light(self, value):
        if value:
            self._state |= 1 << 2
        else:
            self._state &= ~(1 << 2)

    def get_br_light_forced(self):
        return bool(self._state & (1 << 3))

    def set_br_light_forced(self, value):
        if value:
            self._state |= 1 << 3
        else:
            self._state &= ~(1 << 3)

    def get_rr_light(self):
        return bool(self._state & (1 << 4))

    def set_rr_light(self, value):
        if value:
            self._state |= 1 << 4
        else:
            self._state &= ~(1 << 4)

    def get_rr_light_forced(self):
        return bool(self._state & (1 << 5))

    def set_rr_light_forced(self, value):
        if value:
            self._state |= 1 << 5
        else:
            self._state &= ~(1 << 5)

    def get_rr_fan(self):
        return bool(self._state & (1 << 6))

    def set_rr_fan(self, value):
        if value:
            self._state |= 1 << 6
        else:
            self._state &= ~(1 << 6)

    def get_rr_fan_forced(self):
        return bool(self._state & (1 << 7))

    def set_rr_fan_forced(self, value):
        if value:
            self._state |= 1 << 7
        else:
            self._state &= ~(1 << 7)


ownet.init('server:4304')

ctl = CtlBR()

alarm = ownet.Sensor('/alarm')
alarm.useCache(False)

ctl.set_br_light_forced(False)
ctl.set_rr_light_forced(False)
ctl.set_rr_fan_forced(False)
#ctl.set_rr_fan_forced(True)
#ctl.set_rr_fan(True)
t1 = time.time()
ctl.knock(3)
ctl.send_state()
ctl.relax()
t2 = time.time()
print 'Seconds elapsed: ', t2 - t1

while 1:
    if 'Ctl_BR' in alarm.entries():
        ctl.refresh_state()
        print '--- {0:08b} ---'.format(ctl._latch)
        print '--- {0:08b} ---'.format(ctl._state)
        print 'BR Leak: ', ctl.get_br_leak()
        print 'RR Leak: ', ctl.get_rr_leak()
        print 'BR Light:', ctl.get_br_light(),
        if ctl.get_br_light_forced():
            print '(forced)'
        else:
            print
        print 'RR Light:', ctl.get_rr_light(),
        if ctl.get_rr_light_forced():
            print '(forced)'
        else:
            print
        print 'RR Fan:  ', ctl.get_rr_fan(),
        if ctl.get_rr_fan_forced():
            print '(forced)'
        else:
            print

ownet.finish()
