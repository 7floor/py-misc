import paho.mqtt.client as mqtt


def bath_rest_rooms(ow):

    def _get_data_safe():
        try:
            return _ow.read('/Ctl_BR/sensed.BYTE').strip()
        except:
            return ''

    _ow = ow
    _mqttc = mqtt.Client("bath rest rooms")
    _mqttc.connect("server", 1883, 60)
    _state = 0

    while True:
        _mqttc.loop(0)
        yield
        d = _get_data_safe()
        if len(d) == 0:
            continue

        new = int(d)
        delta = new ^ _state

        if delta & (1 << 0):
            v = 0 if new & (1 << 0) else 1
            _mqttc.publish('home/bathroom/leak', v, 2, True)

        if delta & (1 << 1):
            v = 0 if new & (1 << 1) else 1
            _mqttc.publish('home/restroom/leak', v, 2, True)

        if delta & (1 << 2):
            v = 0 if new & (1 << 2) else 1
            _mqttc.publish('home/bathroom/light', v, 2, True)

        if delta & (1 << 4):
            v = 0 if new & (1 << 4) else 1
            _mqttc.publish('home/restroom/light', v, 2, True)

        if delta & (1 << 6):
            v = 0 if new & (1 << 6) else 1
            _mqttc.publish('home/restroom/fan', v, 2, True)

        _state = new
