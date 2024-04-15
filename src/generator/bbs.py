import sympy
import numpy as np

class BlumBlumShub:
  @staticmethod
  def _next_usable_prime(x: int) -> int:
    p = sympy.nextprime(x)
    while (p % 4 != 3):
        p = sympy.nextprime(p)
    return p

  # We define two big numbers and find the appropiate
  # parameters based on them
  p = _next_usable_prime(8*10**8)
  q = _next_usable_prime(4*10**8)
  M = p * q

  def __init__(self, seed):
    self._curr = seed

  def generate(self, amount: int) -> np.array:
    arr = [0] * amount
    for i in range(amount):
      arr[i] = next(self)
    return np.array(arr)

  def __next__(self) -> float:
    self._curr = pow(self._curr, 2, self.M)

    return self._curr / self.M

  def __iter__(self):
    return self