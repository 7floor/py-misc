import paho.mqtt.client as mqtt
import pyownet.protocol as onewire
import owalarm
import time


class Ds2408:

    def __init__(self, ow, owname, mqname):
        self._ow = ow
        self._name = owname
        self._mqttc = mqtt.Client(mqname)
        self._mqttc.connect("server", 1883, 60)

        self._control = False
        self._sequential_alarms_count = 0

        self._reset()
        new = self._read_sensed()
        old = new ^ 0xFF
        self._process_data(old, new)
        self._old = new

    def _reset(self):
        self._ow.write('/'+self._name+'/out_of_testmode', onewire.str2bytez("1"))
        self._ow.write('/'+self._name+'/por', onewire.str2bytez("0"))
        self._ow.write('/'+self._name+'/set_alarm', onewire.str2bytez("133333333"))
        self._ow.write('/'+self._name+'/PIO.BYTE', onewire.str2bytez("0"))
        self._flush_latch()
        self._sequential_alarms_count = 0

    def _write_pio(self, b):
        self._ow.write('/'+self._name+'/PIO.BYTE', onewire.str2bytez(str(~b & 0xFF)))

    def _read_sensed(self):
        s = self._ow.read('/'+self._name+'/sensed.BYTE').strip()
        if s == '':
            return self._old
        else:
            return int(s)

    def _read_latch(self):
        s = self._ow.read('/'+self._name+'/latch.BYTE').strip()
        if s == '':
            return 0
        else:
            return int(s)

    def _flush_latch(self):
        self._ow.write('/'+self._name+'/latch.BYTE', onewire.str2bytez("0"))

    def _process_data(self, old, new):
        pass

    def _on_alarm(self):
        self._sequential_alarms_count += 1
        if self._sequential_alarms_count > 5:  # probably POR, check it
            if self._ow.read('/'+self._name+'/por').strip() == "1":
                self._reset()
                localtime = time.localtime()
                timestring = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
                print timestring, self._name, "por detected -> reset performed"
                yield
                return

        latch = self._read_latch()
        self._flush_latch()
        new = self._read_sensed()

        np = new ^ latch
        if np != self._old and np != new:
            self._process_data(self._old, np)
            self._old = np
        if new != self._old:
            self._process_data(self._old, new)
            self._old = new

        yield

    def _on_control(self):
        pass

    def _is_control(self):
        return False

    def _sleep(self, sec):
        t = time.time()
        while True:
            self._mqttc.loop(0)
            yield
            if time.time() - t >= sec:
                break

    def run(self):
        while True:
            #print self._sequential_alarms_count
            self._mqttc.loop(0)
            yield
            if self._is_control():
                yield self._on_control()
            elif self._name in owalarm.alarms:
                yield self._on_alarm()
            else:
                self._sequential_alarms_count = 0
