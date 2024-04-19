from abc import abstractmethod

from relative_position import forward, still
from stoplight import StopLight
from rectangle import Rectangle
from vehicle.vehicle import Vehicle

class TurningVehicle(Vehicle):
    def think(self, crosswalk_zone: Rectangle, pedestrian_stop_light: StopLight):
        if self._crossing or pedestrian_stop_light.is_green():
            self._desired_movement = forward(self._vel)
        else:
            dist = self.driver_pos.calc_dist_to_zone(still(), crosswalk_zone)
            if dist is None:
                self._desired_movement = forward(self._vel)
            else:
                self._desired_movement = forward(min(dist, self._vel))
