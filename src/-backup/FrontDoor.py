import paho.mqtt.client as mqtt


def front_door(ow):

    def _get_data_safe():
        try:
            return _ow.read('/Ctl_FrontDoor/sensed.BYTE').strip()
        except:
            return ''

    def _get_lock_pos(byte, shift):
        if not (byte & (1 << (shift + 2))):
            return 3
        elif not (byte & (1 << (shift + 1))):
            return 2
        elif not (byte & (1 << (shift + 0))):
            return 1
        else:
            return 0

    _ow = ow

    _mqttc = mqtt.Client("front door")
    _mqttc.connect("server", 1883, 60)

    old = 0
    while True:
        _mqttc.loop(0)
        yield
        d = _get_data_safe()
        if len(d) == 0:
            continue

        new = int(d)
        delta = new ^ old

        if delta & (7 << 0):
            pos = _get_lock_pos(new, 0)
            _mqttc.publish('home/front door/lock/upper', pos, 2, True)

        if delta & (7 << 3):
            pos = _get_lock_pos(new, 3)
            _mqttc.publish('home/front door/lock/lower', pos, 2, True)

        if delta & (1 << 6):
            door = 'open' if new & (1 << 6) else 'closed'
            _mqttc.publish('home/front door/door', door, 2, True)

        if delta & (1 << 7):
            button = 'released' if new & (1 << 7) else 'pressed'
            _mqttc.publish('home/front door/button', button, 2, True)

        old = new
