from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
from typing import List

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

    def is_pedestrian(self) -> bool:
        return not self.is_vehicle()
    
    @abstractmethod
    def plot_in_ax(self, ax: plt.Axes) -> List[AxesImage]:
        pass