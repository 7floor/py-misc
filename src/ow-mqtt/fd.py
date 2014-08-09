from ds2408 import Ds2408


def _get_lock_pos(byte, shift):
    if not (byte & (1 << (shift + 2))):
        return 3
    elif not (byte & (1 << (shift + 1))):
        return 2
    elif not (byte & (1 << (shift + 0))):
        return 1
    else:
        return 0


class Fd(Ds2408):
    def __init__(self, ow):
        Ds2408.__init__(self, ow, "Ctl_FrontDoor", "front door")
        self._mqttc.on_message = self.mqtt_on_message
        self._mqttc.subscribe("home/front door/alarm", 0)
        self._alarm = ""

    def mqtt_on_message(self, mqttc, obj, msg):
        if msg.topic == "home/front door/alarm": # L - light, S - sound, LS - both, B - beep once
            self._alarm = msg.payload

    def _is_control(self):
        return self._alarm in ["L", "S", "LS", "B"]

    def _on_control(self):
        while True:
            if self._alarm == "LS":
                pattern = [0b00000001, 0b10000010, 0b00000100, 0b00001000, 0b10010000, 0b00100000]
            elif self._alarm == "L":
                pattern = [0b00000001, 0b00000010, 0b00000100, 0b00001000, 0b00010000, 0b00100000]
            elif self._alarm == "S":
                pattern = [0b00000000, 0b10000000, 0b00000000, 0b00000000, 0b10000000, 0b00000000]
            elif self._alarm == "B":
                pattern = [0b10111111]
            else:
                break
            for b in pattern:
                self._write_pio(~b & 0xff)
                yield self._sleep(0.1)
                self._write_pio(0xff)
                new = self._read_sensed()
                if new != self._old:
                    self._process_data(self._old, new)
                    self._old = new
                if not self._is_control():
                    break
            # Beep is one time
            if self._alarm == "B":
                self._alarm = ""
                break
        self._flush_latch()

    def _process_data(self, old, new):
        delta = new ^ old

        if delta & (7 << 0):
            pos = _get_lock_pos(new, 0)
            self._mqttc.publish('home/front door/lock/upper', pos, 2, True)

        if delta & (7 << 3):
            pos = _get_lock_pos(new, 3)
            self._mqttc.publish('home/front door/lock/lower', pos, 2, True)

        if delta & (1 << 6):
            door = 'open' if new & (1 << 6) else 'closed'
            self._mqttc.publish('home/front door/door', door, 2, True)

        if delta & (1 << 7):
            button = 'released' if new & (1 << 7) else 'pressed'
            self._mqttc.publish('home/front door/button', button, 2, True)

