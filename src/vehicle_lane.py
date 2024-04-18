from typing import Tuple

from relative_grid import RelativeGrid

from generator.tp_generator import TPGenerator
from stoplight import StopLight

from relative_position import RelativePosition
from directions import Direction
from vehicle import Vehicle
from rectangle import Rectangle

gen = TPGenerator(3*10**6)

class VehicleLane:
    def __init__(self,
                 arrival_rate: int,
                 vehicle_prototype: Rectangle, 
                 crosswalk_zone: Rectangle,
                 pedestrian_stop_light: StopLight,
                 rel_grid: RelativeGrid):
        self._vehicle_prototype = vehicle_prototype
        self._crosswalk_zone = crosswalk_zone
        self._rel_grid = rel_grid
        self._waiting_vehicles = 0
        self._arrival_rate = arrival_rate
        self._pedestrian_stop_light = pedestrian_stop_light

    def _generate_vehicle(self):
        self._waiting_vehicles += gen.poi(self._arrival_rate)

    @property
    def facing(self) -> Direction:
        return self._rel_grid.facing

    def _can_place_vehicle(self) -> bool:
        for i in range(self._rel_grid.cols):
            dist_to_next = self._rel_grid.calc_dist_to_next(RelativePosition.right(i))
            if dist_to_next is not None and dist_to_next < self._vehicle_prototype.rows:
                return False
        return True
    
    def _place_vehicle(self):
        if self._waiting_vehicles == 0 or not self._can_place_vehicle():
            return
        
        offset = (self._rel_grid.cols - self._vehicle_prototype.cols) // 2
        
        vehicle_origin = self._rel_grid.new_displaced(RelativePosition.right(offset))
        Vehicle(vehicle_origin, self._crosswalk_zone, self._vehicle_prototype)
        
    def update(self):
        self._generate_vehicle()
        self._place_vehicle()
