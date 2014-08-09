#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import paho.mqtt.client as mqtt
from bottle import *
from json import dumps

import gevent
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.monkey import patch_all
patch_all()  # this also patches the mqtt!!

app = Bottle()
sockets = set()
data = dict()


def transform_payload(topic, payload):
    if '/temperature/' in topic:
        try:
            return "{0:.1f}°C".format(float(payload))
        except:
            pass
    if '/front door/door' in topic:
        if payload == 'open': return 'Открыта'
        if payload == 'closed': return 'Закрыта'
    if '/front door/lock' in topic:
        if payload == '0':
            return 'Открыт'
        else:
            return 'Закрыт на {0} об.'.format(payload)
    if '/front door/button' in topic:
        if payload == 'pressed': return 'Нажата'
        if payload == 'released': return 'Не нажата'
    if '/light' in topic or '/fan' in topic:
        if payload == '0': return 'Выкл.'
        if payload == '1': return 'Вкл.'
    if '/leak' in topic:
        if payload == '0': return 'Нет'
        if payload == '1': return 'Есть'
    return payload


def update_clients_count():
    send_to_all('dashboard-status', str(len(sockets)) + ' client(s)')


def send_to_all(key, value):
    for socket in set(sockets):  # make copy here because sockets set can be modified by removing failed sockets
        send_to_socket(socket, key, value)


def send_to_socket(socket, key, value):
    try:
        socket.send(dumps({'key': key, 'value': value}, ensure_ascii=False, encoding='utf8'))
    except WebSocketError:
        sockets.remove(socket)
        print 'disconnected, clients:', len(sockets)
        update_clients_count()


def mqtt_on_message(mqttc, obj, msg):
    key, value = msg.topic, transform_payload(msg.topic, msg.payload)
    data[key] = value
    gevent.spawn(send_to_all, key, value)


def mqtt_worker():
    mqttc = mqtt.Client("dashboard")
    mqttc.on_message = mqtt_on_message
    mqttc.connect("server", 1883, 60)
    mqttc.subscribe("home/#", 2)
    try:
        while True:
            mqttc.loop()  # requires gevent monkey patch
    except:
        print 'exiting from mqtt_worker due to exception'
        mqttc.disconnect()
        raise


@app.route('/<folder:re:(js)|(fonts)|(css)>/<filename:path>')
def send_static(folder, filename):
    return static_file(filename, root='./' + folder)


@app.get('/')
@view('index')
def index():
    pass


@app.route('/ws')
def handle_websocket():
    global sockets

    print "Request to websocket, showing HTTP header:"
    for key in request.headers:
        print "  {0}={1}".format(key, request.headers[key])

    ws = request.environ.get('wsgi.websocket')
    if not ws:
        print 'bad websocket request, aborting'
        abort(400, 'Expected WebSocket request.')
    sockets.add(ws)
    print 'connected, clients:', len(sockets)
    for topic in data:
        send_to_socket(ws, topic, data[topic])
    update_clients_count()
    while ws in sockets:
        gevent.sleep(1)


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
print 'Started'

gevent.spawn(mqtt_worker)
#server = WSGIServer(("0.0.0.0", 8080), app, handler_class=WebSocketHandler, certfile='server.crt', keyfile='server.key')
server = WSGIServer(("0.0.0.0", 8080), app, handler_class=WebSocketHandler)
server.serve_forever()
