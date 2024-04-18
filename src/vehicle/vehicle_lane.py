from grid.relative_grid import RelativeGrid

from generator.tp_generator import TPGenerator
from stoplight import StopLight

from relative_position import RelativePosition
from directions import Direction
from vehicle.vehicle import Vehicle
from rectangle import Rectangle
from config import Config

gen = TPGenerator(3 * 10 ** 6)


class VehicleLane:
    def __init__(self,
                 config: Config,
                 rel_grid: RelativeGrid):
        self._config = config
        self._rel_grid = rel_grid
        self._waiting_vehicles = 0

    def _generate_vehicle(self):
        self._waiting_vehicles += gen.poi(self._config.vehicle_arrival_rate)

    @property
    def facing(self) -> Direction:
        return self._rel_grid.facing

    def _can_place_vehicle(self) -> bool:
        for i in range(self._rel_grid.cols):
            dist_to_next = self._rel_grid.calc_dist_to_next(RelativePosition.right(i))
            if dist_to_next is not None and dist_to_next < self._config.vehicle_prot.rows:
                return False
        return True

    def _place_vehicle(self):
        if self._waiting_vehicles == 0 or not self._can_place_vehicle():
            return

        offset = (self._rel_grid.cols - self._config.vehicle_prot.cols) // 2

        vehicle_grid = self._rel_grid.new_displaced(RelativePosition.right(offset))
        Vehicle(vehicle_grid, self._config.vehicle_prot)

    def update(self):
        self._generate_vehicle()
        self._place_vehicle()
