import numpy as np

from .generator import Generator
from .bbs import BlumBlumShub

class TPGenerator(Generator):
  def __init__(self, seed: int):
    self._base_gen = BlumBlumShub(seed)

  def random(self) -> float:
    return next(self._base_gen)

  def randint(self, a: int, b: int) -> int:
    value = self.random()
    value = (b - a) * value + a
    return int(value)

  def poi(self, l: float) -> int:
    # Algorithm taken from https://en.wikipedia.org/wiki/Poisson_distribution#Random_variate_generation

    L = np.exp(-l)
    k = 0
    p = 1
    while True:
      k += 1
      p *= self.random()
      if p <= L:
        return k - 1