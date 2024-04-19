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
        self._vel = 5
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
            dist_to_next = self.driver_pos.calc_dist_to_next(right(i))
            if dist_to_next is not None and dist_to_next < self._vel:
                return False

        return True

    def is_pedestrian_ahead(self) -> bool:
        for i in range(self._width):
            entity = self.driver_pos.get_next(right(i))
            if entity is not None and not entity.is_vehicle():
                return True
        return False
    
    def is_vehicle_ahead(self) -> bool:
        for i in range(self._width):
            entity = self.driver_pos.get_next(right(i))
            if entity is not None and entity.is_vehicle():
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
        
        if self.is_vehicle_ahead():
            return False

        if not self.driver_pos.is_inbounds(self._desired_movement):
            self.remove()
            return False

        self.driver_pos.move(self._desired_movement)

        for rel_grid_i in self.relative_origins:
            rel_grid_i.move(self._desired_movement)

        if not self._crossing:
            self._crossing = self.driver_pos.is_in(crosswalk_zone)
        return False

    def __repr__(self):
        return self._repr

    def remove(self):
        self.driver_pos.clear()
        for rel_grid_i in self.relative_origins:
            rel_grid_i.clear()


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
