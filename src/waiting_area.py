from typing import TypeVar, Generic

from pedestrian import Pedestrian
from generator.tp_generator import TPGenerator

gen = TPGenerator(2**10**7)

T = TypeVar("T")

class WaitingArea(Generic[T]):
    def __init__(self, arrival_rate: float, rel_grid: T):
        self._rel_grid = rel_grid
        self._waiting_pedestrians = 0
        self._arrival_rate = arrival_rate
        self._total_generated_pedestrians = 0

    def _generate_pedestrians(self):
        new_pedestrians = gen.poi(self._arrival_rate)
        self._waiting_pedestrians += new_pedestrians
        self._total_generated_pedestrians += new_pedestrians


    def _move_pedestrians(self):
        while self._waiting_pedestrians > 0:
            if not self._rel_grid.spawn(Pedestrian(self._rel_grid._facing)):
                break
            self._waiting_pedestrians -= 1

    def update(self):
        self._generate_pedestrians()
        self._move_pedestrians()