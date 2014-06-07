from ds2408 import Ds2408


class Brr(Ds2408):
    def __init__(self, ow):
        Ds2408.__init__(self, ow, "Ctl_BR", "bath rest rooms")

    def _process_data(self, old, new):
        #print "BR:", old, new

        delta = new ^ old

        if delta & (1 << 0):
            v = 0 if new & (1 << 0) else 1
            self._mqttc.publish('home/bathroom/leak', v, 2, True)

        if delta & (1 << 1):
            v = 0 if new & (1 << 1) else 1
            self._mqttc.publish('home/restroom/leak', v, 2, True)

        if delta & (1 << 2):
            v = 0 if new & (1 << 2) else 1
            self._mqttc.publish('home/bathroom/light', v, 2, True)

        if delta & (1 << 4):
            v = 0 if new & (1 << 4) else 1
            self._mqttc.publish('home/restroom/light', v, 2, True)

        if delta & (1 << 6):
            v = 0 if new & (1 << 6) else 1
            self._mqttc.publish('home/restroom/fan', v, 2, True)

