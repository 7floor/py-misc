#! /usr/bin/env python
# -*- coding: utf-8 -*-

from candles import Candles
from generators import Generators
from patterns import *
from mplayer import *
from bottle import *
import gevent
from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
patch_all()

os.system('./setup_gpio')

candles = Candles()
gevent.spawn(candles.run)

generators = Generators(candles)
generators.add(p_random1, 5)
generators.add(p_30years_one_dot)
generators.add(p_random1)
generators.add(p_30years_fill)
generators.add(p_random1)
generators.add(p_2x3scroll, 3)
generators.add(p_random1)
generators.add(p_random_up)
generators.add(p_random29, 10)
gevent.spawn(generators.run)

MPlayer.populate()
mp = MPlayer()
mp.loadlist('playlist')

app = Bottle()


@app.route('/<folder:re:(js)|(fonts)|(css)|(img)>/<filename:path>')
def send_static(folder, filename):
    return static_file(filename, root='./' + folder)


@app.get('/')
@view('index')
def index():
    pass


@app.get('/fireplay')
def fireplay():
    generators.paused = False
    redirect('/')


@app.get('/firepause')
def firepause():
    generators.paused = True
    redirect('/')


@app.get('/firereset')
def firereset():
    generators.reset = True
    redirect('/')


@app.get('/playpause')
def songplaypause():
    mp.pause()
    redirect('/')


@app.get('/next')
def songnext():
    mp.pt_step(1)
    redirect('/')


@app.get('/prev')
def songprev():
    mp.pt_step(-1)
    redirect('/')


@app.get('/reset')
def songreset():
    mp.loadlist('playlist')
    redirect('/')


server = WSGIServer(("0.0.0.0", 8080), app)
server.serve_forever()
