import time
from pin import Pin


class Candles:
    groups = []
    lines = []
    candles = []

    def __init__(self):
        self.groups = [Pin('gr{0}'.format(i)) for i in range(6)]
        self.lines = [Pin('ln{0}'.format(i)) for i in range(5)]
        self.candles = [0]*30

    def __del__(self):
        for p in self.groups:
            del p
        for p in self.lines:
            del p

    def show(self, value):
        self.candles = [1 if i < len(value) and str(value[i]) == '1' else 0 for i in range(30)]

    def run(self):
        while True:
            for g in range(6):
                #setup lines
                for l in range(5):
                    self.lines[l].set(self.candles[g*5+l])
                # enable group for some time
                self.groups[g].set(1)
                time.sleep(0.0001)
                self.groups[g].set(0)