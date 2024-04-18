from typing import Tuple

from grid import Grid, CellAlreadyFill
from relative_grid import RelativeGrid
from rectangle import Rectangle
from pedestrian import Pedestrian
from waiting_area import WaitingArea
from generator.tp_generator import TPGenerator
from stoplight import StopLight
from vehicle_lane import VehicleLane

gen = TPGenerator(9*10**7)

class Automata:
    def __init__(self, crosswalk_rows: int, crosswalk_cols: int):
        crosswalk_prototype = Rectangle(crosswalk_rows, crosswalk_cols)
        vehicle_lane_prototype = Rectangle(3*6+crosswalk_prototype.rows, 7)
        waiting_area_prototype = Rectangle(crosswalk_rows, 1)
        car_prototype = Rectangle(6, 5)

        total_rows = vehicle_lane_prototype.rows
        total_cols = crosswalk_cols + 2*waiting_area_prototype.cols
        self._grid = Grid[Pedestrian](total_rows, total_cols)
        self._pedestrian_stop_light = StopLight(90, 20, "green")

        crosswalk = crosswalk_prototype.duplicate()
        crosswalk.move_right(waiting_area_prototype.cols)
        crosswalk.move_down(6)
        self._crosswalk_zone = crosswalk
        print(f"Crosswalk zone: {self._crosswalk_zone}")
        self.build_vehicle_lanes(self._crosswalk_zone, 
                                 car_prototype, 
                                 vehicle_lane_prototype, 
                                 waiting_area_prototype)
        
        walking_zone = Rectangle(crosswalk.rows, crosswalk.cols + 2*waiting_area_prototype.cols)
        walking_zone.move_down(6)
        self.build_waiting_areas(walking_zone)

        self._moved_pedestrians = set()

    def build_waiting_areas(self, walking_zone: Rectangle):

        grid_area_west = RelativeGrid(walking_zone.upper_left, walking_zone, "East", self._grid)
        grid_area_east = RelativeGrid(walking_zone.lower_right, walking_zone, "West", self._grid)

        self._waiting_area_west = WaitingArea(1000/3600, grid_area_west)
        self._waiting_area_east = WaitingArea(1000/3600, grid_area_east)
        


    def build_vehicle_lanes(self,
                            crosswalk_zone: Rectangle,
                            car_prototype: Rectangle,
                            car_lane_zone_prototype: Rectangle,
                            waiting_area_prototype: Rectangle):
        car_lanes_amount = crosswalk_zone.cols // car_lane_zone_prototype.cols
        waiting_area_length = waiting_area_prototype.cols

        self._car_lanes = []
        for i in range(car_lanes_amount//2, car_lanes_amount):
            car_lane_zone = car_lane_zone_prototype.duplicate()
            car_lane_zone.move_right(waiting_area_length + i*car_lane_zone_prototype.cols)
            grid_car_lane = RelativeGrid(car_lane_zone.lower_left, car_lane_zone, "North", self._grid)
            self._car_lanes.append(VehicleLane(1400/(6*3600), car_prototype, crosswalk_zone, self._pedestrian_stop_light, grid_car_lane))
        for i in range(car_lanes_amount//2):
            car_lane_zone = car_lane_zone_prototype.duplicate()
            car_lane_zone.move_right(waiting_area_length + i*car_lane_zone_prototype.cols)
            grid_car_lane = RelativeGrid(car_lane_zone.upper_right, car_lane_zone, "South", self._grid)
            self._car_lanes.append(VehicleLane(1400/(6*3600), car_prototype, crosswalk_zone, self._pedestrian_stop_light, grid_car_lane))

    def update(self):
        self._pedestrian_stop_light.update()
        self._waiting_area_east.update()
        self._waiting_area_west.update()

        # self.show()
        self._grid.apply(lambda object, _: object.think(self._crosswalk_zone, self._pedestrian_stop_light))
        
        self._grid.apply(self.move_object)

        for car_lane in self._car_lanes:
            car_lane.update()
        
        self._moved_pedestrians.clear()

    def move_object(self, object, _: Tuple[int, int]):
        if object in self._moved_pedestrians:
            return
        try:
            object.move(self._crosswalk_zone)
        except CellAlreadyFill:
            pass
        self._moved_pedestrians.add(object)

    def show(self):
        self._pedestrian_stop_light.show()
        print("Waiting at East:", self._waiting_area_east)
        print("Waiting at West:", self._waiting_area_west)
        
        self._grid.show()

