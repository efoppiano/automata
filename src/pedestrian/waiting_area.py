from typing import Optional

from pedestrian.pedestrian import Pedestrian
from generator.tp_generator import poi, randint
from grid.relative_grid import RelativeGrid
from relative_position import right
from stoplight import StopLight


class WaitingArea:
    def __init__(self, arrival_rate: float, rel_grid: RelativeGrid, max_size: int = 100):
        self._rel_grid = rel_grid
        self._waiting_pedestrians = 0
        self._arrival_rate = arrival_rate
        self._total_generated_pedestrians = 0
        self._max_size = max_size

    def _generate_pedestrians(self):
        if self._waiting_pedestrians == self._max_size:
            return
        
        new_pedestrians = min(self._max_size - self._waiting_pedestrians, poi(self._arrival_rate))
        self._waiting_pedestrians += new_pedestrians
        self._total_generated_pedestrians += new_pedestrians


    def _can_place_pedestrian(self) -> bool:
        for i in range(self._rel_grid.rows):
            if not self._rel_grid.is_fill(right(i)):
                return True
        return False
    
    def _place_pedestrian(self):
        rows = self._rel_grid.rows
        
        possible_pos = randint(0, rows)
        while self._rel_grid.is_fill(right(possible_pos)):
            possible_pos = (possible_pos + 1) % rows

        pedestrian_grid = self._rel_grid.new_displaced(right(possible_pos))
        self._rel_grid.fill(right(possible_pos), Pedestrian(pedestrian_grid))

        self._waiting_pedestrians -= 1
    
    def _place_pedestrians(self):
        while self._waiting_pedestrians > 0 and self._can_place_pedestrian():
            self._place_pedestrian()

    def update(self, pedestrian_stop_light: Optional[StopLight] = None):
        self._generate_pedestrians()
        if pedestrian_stop_light is None or pedestrian_stop_light.is_green():
            self._place_pedestrians()
            
            

    def __repr__(self) -> str:
        return f"{self._waiting_pedestrians : <3}"