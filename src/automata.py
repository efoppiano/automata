from typing import Tuple

from grid import Grid, CellAlreadyFill
from relative_grid import RelativeGrid
from rectangle import Rectangle
from pedestrian import Pedestrian
from waiting_area import WaitingArea
from generator.tp_generator import TPGenerator
from semaphore import Semaphore
from vehicle_lane import VehicleLane

gen = TPGenerator(9*10**7)

class Automata:
    def __init__(self, crosswalk_rows: int, crosswalk_cols: int):
        crosswalk_prototype = Rectangle(crosswalk_cols, crosswalk_rows)
        vehicle_lane_prototype = Rectangle(7, 2*5+crosswalk_prototype.width)
        waiting_area_prototype = Rectangle(0, crosswalk_rows)
        car_prototype = Rectangle(5, 6)

        total_rows = vehicle_lane_prototype.width
        total_cols = crosswalk_cols + 2*waiting_area_prototype.length
        self._grid = Grid[Pedestrian](total_rows, total_cols)
        self._pedestrian_sem = Semaphore(20, 10, "red")

        self.build_vehicle_lanes(crosswalk_prototype, 
                                 car_prototype, 
                                 vehicle_lane_prototype, 
                                 waiting_area_prototype)
        self.build_crosswalk(crosswalk_prototype, waiting_area_prototype, vehicle_lane_prototype)

        self._moved_pedestrians = set()

    def build_crosswalk(self,
                        crosswalk_prototype: Rectangle,
                        waiting_area_prototype: Rectangle,
                        vehicle_lane_prototype: Rectangle):
        crosswalk = crosswalk_prototype.duplicate()
        crosswalk.move_right(waiting_area_prototype.length)
        crosswalk.move_down(vehicle_lane_prototype.width)
        print(f"Pedestrian zone: {crosswalk}")
        
        grid_area_west = RelativeGrid(crosswalk.upper_left, crosswalk, "East", self._grid)
        grid_area_east = RelativeGrid(crosswalk.lower_right, crosswalk, "West", self._grid)

        self._waiting_area_west = WaitingArea(500/360, grid_area_west, self._pedestrian_sem)
        self._waiting_area_east = WaitingArea(500/360, grid_area_east, self._pedestrian_sem)
        


    def build_vehicle_lanes(self,
                            crosswalk_prototype: Rectangle,
                            car_prototype: Rectangle,
                            car_lane_zone_prototype: Rectangle,
                            waiting_area_prototype: Rectangle):
        car_lanes_amount = crosswalk_prototype.length // car_lane_zone_prototype.length
        waiting_area_length = waiting_area_prototype.length

        self._car_lanes = []
        for i in range(car_lanes_amount//2):
            car_lane_zone = car_lane_zone_prototype.duplicate()
            car_lane_zone.move_right(waiting_area_length + i*car_lane_zone_prototype.length)
            grid_car_lane = RelativeGrid(car_lane_zone.lower_left, car_lane_zone, "North", self._grid)
            self._car_lanes.append(VehicleLane(500/3600, car_prototype.length, car_prototype.width, self._pedestrian_sem, grid_car_lane))
        for i in range(car_lanes_amount//2, car_lanes_amount):
            car_lane_zone = car_lane_zone_prototype.duplicate()
            car_lane_zone.move_right(waiting_area_length + i*car_lane_zone_prototype.length)
            grid_car_lane = RelativeGrid(car_lane_zone.upper_right, car_lane_zone, "South", self._grid)
            self._car_lanes.append(VehicleLane(500/3600, car_prototype.length, car_prototype.width, self._pedestrian_sem, grid_car_lane))

    def update(self):
        self._pedestrian_sem.update()
        # self._waiting_area_east.update()
        # self._waiting_area_west.update()
        for car_lane in self._car_lanes:
            car_lane.update()
        
        # self.show()
        # self._grid.apply(lambda pedestrian, _: pedestrian.think(self._pedestrian_sem))
        
        # self._grid.apply(self.move_pedestrian)
        
        self._moved_pedestrians.clear()

    def move_pedestrian(self, pedestrian: Pedestrian, _: Tuple[int, int]):
        if pedestrian in self._moved_pedestrians:
            return
        try:
            pedestrian.move()
        except CellAlreadyFill:
            pass
        self._moved_pedestrians.add(pedestrian)

    def show(self):
        self._pedestrian_sem.show()
        print("Waiting at East:", self._waiting_area_east)
        print("Waiting at West:", self._waiting_area_west)
        
        self._grid.show()

