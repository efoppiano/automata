from typing import TypeVar

from pedestrian import Pedestrian
from generator.tp_generator import TPGenerator
from stoplight import StopLight
from relative_grid import RelativeGrid
from relative_position import RelativePosition

gen = TPGenerator(2**10**7)


class WaitingArea:
    def __init__(self, arrival_rate: float, rel_grid: RelativeGrid, pedestrian_stop_light: StopLight, max_size: int = 100):
        self._rel_grid = rel_grid
        self._waiting_pedestrians = 0
        self._arrival_rate = arrival_rate
        self._total_generated_pedestrians = 0
        self._pedestrian_stop_light = pedestrian_stop_light
        self._max_size = max_size

    def _generate_pedestrians(self):
        if self._waiting_pedestrians == self._max_size:
            return
        
        new_pedestrians = min(self._max_size - self._waiting_pedestrians, gen.poi(self._arrival_rate))
        self._waiting_pedestrians += new_pedestrians
        self._total_generated_pedestrians += new_pedestrians


    def _can_place_pedestrian(self) -> bool:
        width = self._rel_grid.width
        for i in range(width):
            if not self._rel_grid.is_fill(RelativePosition.right(i), ignore_opposite_direction=False):
                return True
        return False
    
    def _place_pedestrian(self):
        width = self._rel_grid.width
        
        possible_pos = gen.randint(0, width)
        while self._rel_grid.is_fill(RelativePosition.right(possible_pos), ignore_opposite_direction=False):
            possible_pos = (possible_pos + 1) % width

        pedestrian_grid = self._rel_grid.new_displaced(RelativePosition.right(possible_pos))
        self._rel_grid.fill(RelativePosition.right(possible_pos), Pedestrian(pedestrian_grid))
        self._waiting_pedestrians -= 1
    
    def _place_pedestrians(self):
        while self._waiting_pedestrians > 0 and self._can_place_pedestrian():
            self._place_pedestrian()

    def update(self):
        self._generate_pedestrians()
        if self._pedestrian_stop_light.state == "green":
            self._place_pedestrians()

    def __repr__(self) -> str:
        return f"{self._waiting_pedestrians : <3}"