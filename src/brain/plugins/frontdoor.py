from plugin import *
from time import time, sleep

# alarm timeout in seconds - allow this time door unlocked before start alarming
timeout = 60


@subscribe('home/front door/lock/#')
def on_lock_changed(message):
    global upper, lower, locked
    if 'upper' in message.topic:
        upper = False if message.payload == "0" else True
    if 'lower' in message.topic:
        lower = False if message.payload == "0" else True
    locked = upper or lower


@execute
def run():
    while True:
        logger.info("door is locked")
        set_alarm(False)
        while locked:
            sleep(0.1)

        logger.info("door is unlocked, will alarm soon")
        t = time()
        while time() - t < timeout and not locked:
            sleep(1)

        if locked:
            continue

        logger.info("alarming")
        set_alarm(True)

        while not locked:
            sleep(0.1)


def set_alarm(on):
    publish("home/front door/alarm", ("LS" if on else "OFF"), 2)


upper = True
lower = True
locked = True
