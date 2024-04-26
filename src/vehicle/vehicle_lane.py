from abc import ABC, abstractmethod

from grid.relative_grid import RelativeGrid

from generator.tp_generator import poi

from relative_position import right
from directions import Direction
from rectangle import Rectangle
from config import Config

from road_entity import RoadEntity


class VehicleLane(ABC):
    def __init__(self,
                 config: Config,
                 rel_grid: RelativeGrid[RoadEntity]):
        self._config = config
        self._rel_grid = rel_grid
        self._waiting_vehicles = 0

    @abstractmethod
    def spawn_vehicle(self, vehicle_grid: RelativeGrid[RoadEntity], vehicle_prot: Rectangle):
        pass

    def _generate_vehicle(self):
        self._waiting_vehicles += poi(self._config.vehicle_arrival_rate)

    @property
    def facing(self) -> Direction:
        return self._rel_grid.facing

    def _can_place_vehicle(self) -> bool:
        for i in range(self._rel_grid.cols):
            dist_to_next = self._rel_grid.calc_dist_to_next(right(i), max_checks=self._config.vehicle_prot.cols)
            if dist_to_next is not None:
                return False
        return True

    def _place_vehicle(self):
        if self._waiting_vehicles == 0 or not self._can_place_vehicle():
            return

        offset = (self._rel_grid.cols - self._config.vehicle_prot.cols) // 2

        vehicle_grid = self._rel_grid.new_displaced(right(offset))
        self.spawn_vehicle(vehicle_grid, self._config.vehicle_prot)
        self._waiting_vehicles -= 1

    def update(self):
        self._generate_vehicle()
        self._place_vehicle()
