from typing import Tuple

from relative_grid import RelativeGrid

from generator.tp_generator import TPGenerator
from semaphore import Semaphore

from relative_position import RelativePosition

gen = TPGenerator(3*10**6)

class VehicleLane:
    def __init__(self, arrival_rate: int, vehicle_width: int, vehicle_length: int, 
                 pedestrian_semaphore: Semaphore, rel_grid: RelativeGrid):
        self._vehicle_width = vehicle_width
        self._vehicle_length = vehicle_length
        self._rel_grid = rel_grid
        self._waiting_vehicles = 0
        self._arrival_rate = arrival_rate
        self._pedestrian_semaphore = pedestrian_semaphore

    def _generate_vehicle(self):
        self._waiting_vehicles += gen.poi(self._arrival_rate)

    def _can_place_vehicle(self) -> bool:
        for i in range(self._rel_grid.length):
            if self._rel_grid.get_next(RelativePosition.right(i)):
                return False
        return True
    
    def _place_vehicle(self):
        if self._waiting_vehicles == 0 or not self._can_place_vehicle():
            return
        
        offset = (self._rel_grid.length - self._vehicle_width) // 2
        print(f"Offset: {offset}")
        
        for i in range(offset, offset + self._vehicle_width):
            for j in range(self._vehicle_length):
                value = "V" if self._rel_grid.facing == "South" else "^"
                self._rel_grid.fill(RelativePosition.right(i) + RelativePosition.forward(j), value)

    def update(self):
        self._generate_vehicle()
        self._place_vehicle()
