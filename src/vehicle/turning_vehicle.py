from abc import abstractmethod

from relative_position import forward, still
from stoplight import StopLight
from rectangle import Rectangle
from vehicle.vehicle import Vehicle

class TurningVehicle(Vehicle):
    def think(self, _crosswalk_zone: Rectangle, _pedestrian_stop_light: StopLight):
        if self.is_entity_ahead():
            self._desired_movement = still()
        else:
            self._desired_movement = forward(self._vel)