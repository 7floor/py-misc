import time
import paho.mqtt.client as mqtt
import pyownet.protocol as onewire


def temperatures(ow, sensors):

    def _poll_mqtt():
        _mqttc.loop(0)

    def _wait_for_start():
        #print 'waiting to measure temperatures'
        while time.localtime().tm_sec % 10 != 0:
            _poll_mqtt()
            yield
        yield time.localtime()

    def _convert_temeratures():
        #print 'start temperature conversion'
        _ow.write('/simultaneous/temperature', onewire.str2bytez('1'))
        yield
        #print 'waiting for temperature conversion ready'
        t = time.time()
        while time.time() - t < 2:
            _poll_mqtt()
            yield

    def _get_temp_safe(s):
        try:
            return _ow.read('/' + s + '/temperature').strip()
        except onewire.Error:
            return ''

    def _get_temperatures():
        yield _convert_temeratures()
        #print 'reading temperatures'
        for k, v in _sensors.iteritems():
            for _ in range(3):
                yield
                temp = _get_temp_safe(k)
                if len(temp) > 0:
                    break
            if len(temp) != 0 and temp != v[1]:
                v[1] = temp
                #_mqttc.publish('home/' + v[0] + '/temperature', temp, 2, True)
                _mqttc.publish('home/temperature/' + v[0], temp, 2, True)

    _ow = ow
    _mqttc = mqtt.Client("thermometers")
    _mqttc.connect("server", 1883, 60)
    _sensors = dict((key, [value, '']) for key, value in sensors.iteritems())

    while True:
        t = yield _wait_for_start()
        yield _get_temperatures()
        _mqttc.publish('home/temperature/measured on', time.strftime("%Y-%m-%d %H:%M:%S", t), 2, True)
        _poll_mqtt()