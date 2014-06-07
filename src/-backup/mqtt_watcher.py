import paho.mqtt.client as mqtt


def mqtt_watcher(*broker):

    def _mqtt_on_message(mqttc, obj, msg):
        print("watcher: " + msg.topic + " " + str(msg.payload))

    _mqttc = mqtt.Client("watcher")
    _mqttc.on_message = _mqtt_on_message
    _mqttc.connect(*broker)
    _mqttc.subscribe("home/#", 2)

    while True:
        _mqttc.loop(0)
        yield
