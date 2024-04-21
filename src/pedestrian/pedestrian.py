from directions import Direction
from grid.relative_grid import RelativeGrid
from generator.tp_generator import random, choice
from relative_position import forward, left, right, still, RelativePosition
from directions import opposite_direction
from stoplight import StopLight
from rectangle import Rectangle

from road_entity import RoadEntity

class Pedestrian(RoadEntity):
    def __init__(self, rel_grid: RelativeGrid[RoadEntity], velocity: int = None, repr: str = None):
        self._desired_displacement = still()
        self._rel_grid = rel_grid
        self._crossing = False

        if velocity is not None:
            self._vel = velocity
        else:
            self._vel = self._generate_velocity()

        if repr is not None:
            self._repr = repr
        else:
            self._repr = choice(["😀", "😁", "🙃", "🤔", "😶", "🙄", "😎"])

    @property
    def facing(self) -> Direction:
        return self._rel_grid.facing
    
    def is_vehicle(self) -> bool:
        return False

    def is_crossing(self) -> bool:
        return self._crossing

    def __repr__(self):
        return self._repr

    def _generate_velocity(self) -> int:
        p = random()
        
        if p > 0.978:
            return 6
        elif p > 0.93:
            return 5
        elif p > 0.793:
            return 4
        elif p > 0.273:
            return 3
        else:
            return 2

    def can_move_forward(self) -> bool:
        if not self._rel_grid.is_inbounds(forward(1)):
            return True
        
        dist_to_next =  self._rel_grid.calc_dist_to_next(still(), lambda ent: ent.is_crossing() and\
                                                         ent.facing == self.facing, 1)
        return dist_to_next is None or dist_to_next >= 1
    
    def can_do_lateral_movement(self, to_right: bool) -> bool:
        displacement = right(1) if to_right else left(1)

        if not self._rel_grid.is_fill(forward(1)):
            return False
        
        if not self._rel_grid.is_inbounds(displacement):
            return False
        
        if self._rel_grid.is_fill(displacement):
            return False
        
        dist = self._rel_grid.calc_dist_to_next(displacement, lambda ent: ent.is_crossing() and\
                                                ent.facing == opposite_direction(self.facing), self._vel)
        if dist is not None:
            return False
        
        dist_to_prev = self._rel_grid.calc_dist_to_prev(displacement, lambda ent: ent.is_crossing() and\
                                                        ent.facing == self.facing, 6)
        if dist_to_prev is None:
            return True
        prev = self._rel_grid.get_prev(displacement, lambda ent: ent.is_crossing() and\
                                       ent.facing == self.facing, 6)
        
        return prev._vel < self._vel
    
    def can_move_left(self) -> bool:
        return self.can_do_lateral_movement(False)
    
    def can_move_right(self) -> bool:
        return self.can_do_lateral_movement(True)

    def _get_pos_forward(self) -> RelativePosition:
        dist_to_next = self._rel_grid.calc_dist_to_next(still(), lambda ent: ent.is_crossing() and\
                                                        ent.facing == self.facing)
        if dist_to_next is None or dist_to_next > self._vel:
            return forward(self._vel)
        return forward(dist_to_next)
    
    def _get_pos_left_right_random(self) -> RelativePosition:
        p = random()
        if p > 0.5:
            return left(1)
        else:
            return right(1)

    def think(self, crosswalk_zone: Rectangle, pedestrian_stop_light: StopLight):
        if pedestrian_stop_light.is_red():
            if not self._rel_grid.is_in(crosswalk_zone):
                self._desired_displacement = still()
                return
            else:
                self._vel = 6
                self._repr = "😰"            
    
        if self.can_move_forward():
            self._desired_displacement = self._get_pos_forward()
        else:
            can_move_left = self.can_move_left()
            can_move_right = self.can_move_right()
            
            if can_move_left and not can_move_right:
                self._desired_displacement = left(1)
            elif can_move_right and not can_move_left:
                self._desired_displacement = right(1)
            elif can_move_left and can_move_right:
                self._desired_displacement = self._get_pos_left_right_random()
            else:
                self._desired_displacement = still()

    # Return True if a conflict is encountered between the pedestrian and a vehicle
    def move(self, crosswalk_zone: Rectangle) -> bool:
        if not self._rel_grid.is_inbounds(self._desired_displacement):
            self._rel_grid.clear()
            return False
        if self._desired_displacement.is_still():
            return False
        self._crossing = True
        if not self._rel_grid.new_displaced(self._desired_displacement).is_in(crosswalk_zone):
            self._rel_grid.clear()
            return False

        while not self._desired_displacement.is_still() and self._rel_grid.is_fill(self._desired_displacement):
            self._desired_displacement.decrease()
        
        if self._desired_displacement.is_still():
            return False
        
        self._rel_grid.move(self._desired_displacement)
        return False