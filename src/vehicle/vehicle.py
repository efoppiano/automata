import matplotlib.pyplot as plt
from matplotlib.image import AxesImage

from images import place_image, squares
from typing import List
from abc import ABC, abstractmethod

from grid.relative_grid import RelativeGrid
from relative_position import forward, right, still
from stoplight import StopLight
from generator.tp_generator import choice
from rectangle import Rectangle
from road_entity import RoadEntity

class Vehicle(RoadEntity, ABC):
    def __init__(self, origin: RelativeGrid[RoadEntity], prototype: Rectangle):
        self._repr = choice(["🟥", "🟧", "🟨", "🟩", "🟦", "🟪", "🟫"])
        self._vel = 10
        self._crossing = False
        self._desired_movement = still()
        self._width = prototype.cols
        self._length = prototype.rows

        self.build_grids(origin)

    def build_grids(self, origin: RelativeGrid[RoadEntity]):
        self.relative_origins: List[RelativeGrid[RoadEntity]] = []
        for i in range(self._width):
            for j in range(self._length):
                origin_ij = origin.new_displaced(
                    right(i) + forward(j)
                )
                if i == 0 and j == self._length - 1:
                    self.driver_pos: RelativeGrid[RoadEntity] = origin_ij
                else:
                    self.relative_origins.insert(0,
                                                 origin_ij)  # We will want to move the last ones first as they're in front

        self.driver_pos.fill(still(), self)
        for rel_grid_i in self.relative_origins:
            part = VehiclePart(self, rel_grid_i, self._repr)
            rel_grid_i.fill(still(), part)

    @property
    def facing(self):
        return self.driver_pos.facing
    
    def is_vehicle(self) -> bool:
        return True
    
    def is_crossing(self) -> bool:
        return self._crossing

    def can_move(self) -> bool:
        for i in range(self._width):
            dist_to_next = self.driver_pos.calc_dist_to_next(right(i), max_checks=self._vel)
            if dist_to_next is not None:
                return False

        return True

    def is_entity_ahead(self) -> bool:
        for i in range(self._width):
            entity = self.driver_pos.get_next(right(i), max_checks=self._vel)
            if entity is not None:
                return True
        return False
    
    def is_pedestrian_ahead(self) -> bool:
        for i in range(self._width):
            entity = self.driver_pos.get_next(right(i), max_checks=self._vel)
            if entity is not None and entity.is_pedestrian():
                return True
        return False
    

    @abstractmethod
    def think(self, crosswalk_zone: Rectangle, pedestrian_stop_light: StopLight):
        pass

    def move(self, crosswalk_zone: Rectangle) -> bool:
        if self._desired_movement.is_still():
            return False
        
        if self.is_pedestrian_ahead():
            for rel_grid_i in self.relative_origins:
                if rel_grid_i.new_displaced(self._desired_movement).is_in(crosswalk_zone):
                    return True
            return False

        if not self.driver_pos.is_inbounds(self._desired_movement):
            self.remove()
            return False

        self._crossing = True
        self.driver_pos.move(self._desired_movement)

        for rel_grid_i in self.relative_origins:
            rel_grid_i.move(self._desired_movement)

        return False

    def __repr__(self):
        return self._repr

    def remove(self):
        self.driver_pos.clear()
        for rel_grid_i in self.relative_origins:
            rel_grid_i.clear()

    def plot_in_ax(self, ax: plt.Axes) -> List[AxesImage]:
        return [place_image(ax, squares[self._repr], self.driver_pos._center[1], self.driver_pos._center[0])]


class VehiclePart(RoadEntity):
    def __init__(self, parent: Vehicle, relative_origin: RelativeGrid[RoadEntity], repr: str):
        self.parent = parent
        self.relative_origin = relative_origin
        self._repr = repr
        self._vel = 0

    @property
    def facing(self):
        return self.relative_origin.facing
    
    def is_vehicle(self) -> bool:
        return True
    
    def is_crossing(self) -> bool:
        return self.parent.is_crossing

    def think(self, _: Rectangle, __: StopLight):
        pass

    def __repr__(self):
        return self._repr

    def move(self, _: Rectangle):
        pass

    def remove(self):
        pass

    def plot_in_ax(self, ax: plt.Axes) -> List[AxesImage]:
        return [place_image(ax, squares[self._repr], self.relative_origin._center[1], self.relative_origin._center[0])]