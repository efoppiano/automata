from typing import TypeVar, Generic

from pedestrian import Pedestrian
from generator.tp_generator import TPGenerator
from semaphore import Semaphore

gen = TPGenerator(2**10**7)

T = TypeVar("T")

class WaitingArea(Generic[T]):
    def __init__(self, arrival_rate: float, rel_grid: T, pedestrian_sem: Semaphore, max_size: int = 100):
        self._rel_grid = rel_grid
        self._waiting_pedestrians = 0
        self._arrival_rate = arrival_rate
        self._total_generated_pedestrians = 0
        self._pedestrian_sem = pedestrian_sem
        self._max_size = max_size

    def _generate_pedestrians(self):
        if self._waiting_pedestrians == self._max_size:
            return
        
        new_pedestrians = min(self._max_size - self._waiting_pedestrians, gen.poi(self._arrival_rate))
        self._waiting_pedestrians += new_pedestrians
        self._total_generated_pedestrians += new_pedestrians


    def _move_pedestrians(self):
        while self._waiting_pedestrians > 0:
            if not self._rel_grid.spawn(Pedestrian(self._rel_grid._facing)):
                break
            self._waiting_pedestrians -= 1

    def update(self):
        self._generate_pedestrians()
        if self._pedestrian_sem.state == "green":
            self._move_pedestrians()

    def __repr__(self) -> str:
        return f"{self._waiting_pedestrians : <3}"