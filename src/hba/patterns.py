import random


def p_30years_one_dot():
    pattern = [1] + [0] * 29
    d = 0
    for i in range(30):
        if i == 0 or i == 15:
            d = 0.08
        d -= 0.07 / 15
        yield (d, pattern)
        pattern.pop()
        pattern.insert(0, 0)


def p_30years_fill():
    pattern = [0] * 30
    d = 0
    for i in range(30):
        pattern[i] = 1
        if i == 0 or i == 15:
            d = 0.08
        d -= 0.07 / 15
        yield (d, pattern)


def p_2x3scroll():
    patterns = ['11000', '01100', '00110', '00011', '10001']
    patterns = [i * 6 for i in patterns]
    for i in range(3):
        for pattern in patterns:
            yield (0.05, pattern)
    for i in range(3):
        for pattern in patterns[::-1]:
            yield (0.05, pattern)


def p_random1():
    for pattern in _random(1, 100):
        yield pattern


def p_random15():
    for pattern in _random(15, 100):
        yield pattern


def p_random29():
    for pattern in _random(29, 100):
        yield pattern


def p_random_up():
    for l in range(1, 30):
        for pattern in _random(l, 30 - l):
            yield pattern


def _random(n, duration):
    pattern = [1] * n + [0] * (30-n)
    for i in range(duration):
        random.shuffle(pattern)
        yield (0.01, pattern)
