from abc import ABC, abstractmethod

from orientable import Orientable
from rectangle import Rectangle
from stoplight import StopLight

class RoadEntity(Orientable, ABC):
    @abstractmethod
    def is_crossing(self) -> bool:
        pass

    @abstractmethod
    def think(self, crosswalk_zone: Rectangle, pedestrian_stop_light: StopLight):
        pass

    @abstractmethod
    def move(self, crosswalk_zone: Rectangle) -> bool:
        pass

    @abstractmethod
    def is_vehicle(self) -> bool:
        pass