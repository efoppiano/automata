from typing import List
from abc import ABC, abstractmethod

from grid.relative_grid import RelativeGrid
from relative_position import forward, still
from stoplight import StopLight
from rectangle import Rectangle
from road_entity import RoadEntity
from vehicle.vehicle import Vehicle

class StraightVehicle(Vehicle):
    def think(self, _crosswalk_zone: Rectangle, pedestrian_stop_light: StopLight):
        if self.is_entity_ahead() or (not pedestrian_stop_light.is_red() and not self._crossing):
            self._desired_movement = still()
        elif self._crossing or pedestrian_stop_light.is_red():
            self._desired_movement = forward(self._vel)
        else:
            self._desired_movement = still()