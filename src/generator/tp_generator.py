import numpy as np

from .generator import Generator
from .bbs import BlumBlumShub

gen = BlumBlumShub(4 * 10 ** 7)

def set_seed(seed: int):
    global gen
    gen = BlumBlumShub(seed)

def random() -> float:
    return next(gen)

def randint(a: int, b: int) -> int:
    value = random()
    value = (b - a) * value + a
    return int(value)

def choice(seq: list):
    return seq[randint(0, len(seq) - 1)]

def poi(l: float) -> int:
    # Algorithm taken from https://en.wikipedia.org/wiki/Poisson_distribution#Random_variate_generation

    L = np.exp(-l)
    k = 0
    p = 1
    while True:
        k += 1
        p *= random()
        if p <= L:
            return k - 1