import pyownet.protocol as onewire
import time
import re

alarms = []


def checkalarm(ow):
    _ow = ow
    r = re.compile(r"/alarm/(.+)/")
    global alarms
    while True:
        try:
            t = time.time()
            alarms = [r.match(str(s)).group(1) for s in _ow.dir('/alarm')]
            #print alarms, time.time() - t
        except onewire.Error as err:
            print err
            pass

        yield
