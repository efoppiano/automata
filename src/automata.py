from typing import Tuple, List

from grid.grid import Grid
from grid.relative_grid import RelativeGrid
from rectangle import Rectangle
from pedestrian.waiting_area import WaitingArea
from road_entity import RoadEntity
from vehicle.turning_vehicle_lane import TurningVehicleLane
from vehicle.straight_vehicle_lane import StraightVehicleLane
from vehicle.vehicle_lane import VehicleLane
from config import Config
from plotter import Plotter

class Automata:
    def __init__(self):
        self._config = Config.new_from_env_file()
        self._grid = Grid[RoadEntity](self._config.total_rows, self._config.total_cols)
        self._crosswalk_zone = Rectangle(self._config.crosswalk_prot.rows, self._config.crosswalk_prot.cols)
        self._crosswalk_zone.move_down(self._config.vehicle_prot.rows)
        self._crosswalk_zone.move_right(self._config.waiting_area_prot.cols)

        self.build_waiting_areas()
        self.build_vehicle_lanes()

        self._epoch = 0
        self._conflicts = 0
        self._entities_with_conflicts = set()
        self._plotter = Plotter(self._grid, self._config)

    def build_waiting_areas(self):
        if self._config.waiting_area_prot.cols > 0:
            walking_zone = Rectangle(self._config.crosswalk_prot.rows, self._config.crosswalk_prot.cols + 2)
            walking_zone.move_right(self._config.waiting_area_prot.cols - 1)
        else:
            walking_zone = Rectangle(self._config.crosswalk_prot.rows, self._config.crosswalk_prot.cols)
        walking_zone.move_down(self._config.vehicle_prot.rows)
            
        grid_area_west = RelativeGrid(walking_zone.upper_left, walking_zone, "East", self._grid)
        grid_area_east = RelativeGrid(walking_zone.lower_right, walking_zone, "West", self._grid)

        self._waiting_areas: List[WaitingArea] = []
        waiting_area_west = WaitingArea(self._config.pedestrian_arrival_rate, grid_area_west)
        waiting_area_east = WaitingArea(self._config.pedestrian_arrival_rate, grid_area_east)

        self._waiting_areas.append(waiting_area_west)
        self._waiting_areas.append(waiting_area_east)
    


    def build_vehicle_lanes(self):
        self._vehicle_lanes: List[VehicleLane] = []
        vehicle_lanes_amount = self._config.crosswalk_prot.cols // self._config.vehicle_lane_prot.cols
        for i in range(vehicle_lanes_amount):
            vehicle_lane_zone = self._config.vehicle_lane_prot.duplicate()
            vehicle_lane_zone.move_right(self._config.waiting_area_prot.cols + i*vehicle_lane_zone.cols)
            
            if i < vehicle_lanes_amount//2:
                facing = "South"
                origin = vehicle_lane_zone.upper_right
            else:
                facing = "North"
                origin = vehicle_lane_zone.lower_left
            
            grid = RelativeGrid(origin, vehicle_lane_zone, facing, self._grid)
            if i == 0 or i == vehicle_lanes_amount - 1:
                vehicle_lane = TurningVehicleLane(self._config, grid)
            else:
                vehicle_lane = StraightVehicleLane(self._config, grid)
            self._vehicle_lanes.append(vehicle_lane)

    def update(self):
        self._config.pedestrian_stop_light.update()
        for waiting_area in self._waiting_areas:
            waiting_area.update()

        self._grid.apply(lambda object, _: object.think(self._crosswalk_zone, self._config.pedestrian_stop_light))
        
        self._grid.apply(self.move_object)

        for vehicle_lane in self._vehicle_lanes:
            vehicle_lane.update()
        
        self._epoch += 1

    def move_object(self, entity: RoadEntity, _: Tuple[int, int]):
        conflict_happened = entity.move(self._crosswalk_zone)
        if conflict_happened:
            self._conflicts += 1


    def show(self):
        print(f"Epoch: {self._epoch}")
        print(f"Conflicts: {self._conflicts}")
        self._config.pedestrian_stop_light.show()
        print("Waiting at East:", self._waiting_areas[0])
        print("Waiting at West:", self._waiting_areas[1])
        
        self._plotter.plot()

    def advance_to(self, epoch: int):
        while self._epoch < epoch:
            self.update()

