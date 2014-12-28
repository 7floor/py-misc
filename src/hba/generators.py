import time


class Generators:
    candles = None
    generators = []
    paused = False
    reset = False

    def __init__(self, candles):
        self.candles = candles

    def add(self, generator, repeat=1):
        self.generators.append((repeat, generator))

    def _generate(self, generator):
        for pattern in generator():
            self.candles.show(pattern[1])
            time.sleep(pattern[0])

    def run(self):
        while True:
            self.reset = self.paused = False
            for generator in self.generators:
                if self.reset:
                    break
                for n in range(generator[0]):
                    if self.reset:
                        break
                    while True:
                        self._generate(generator[1])
                        if self.reset or not self.paused:
                            break
