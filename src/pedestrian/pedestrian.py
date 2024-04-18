from directions import Direction
from grid.relative_grid import RelativeGrid
from generator.tp_generator import TPGenerator
from relative_position import RelativePosition
from directions import opposite_direction
from stoplight import StopLight
from rectangle import Rectangle

from orientable import Orientable

gen = TPGenerator(4*10**7)

class Pedestrian(Orientable):
    def __init__(self, rel_grid: RelativeGrid, velocity: int = None, repr: str = None):
        self._desired_displacement = None
        self._rel_grid = rel_grid

        if velocity is not None:
            self._vel = velocity
        else:
            self._vel = self._generate_velocity()

        if repr is not None:
            self._repr = repr
        else:
            self._repr = gen.choice(["😀", "😁", "🙃", "🤔", "😶", "🙄", "😎"])

    @property
    def facing(self) -> Direction:
        return self._rel_grid.facing
    
    def __repr__(self):
        return self._repr

    def _generate_velocity(self) -> int:
        p = gen.random()
        
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
        return not self._rel_grid.is_fill(RelativePosition.forward(1))
    
    def can_move_left(self) -> bool:
        if not self._rel_grid.is_inbounds(RelativePosition.left(1)):
            return False
        
        if self._rel_grid.is_fill(RelativePosition.left(1)):
            return False
        
        prev = self._rel_grid.get_prev(RelativePosition.left(1),
                                       lambda obj: obj.facing == self.facing)
        if prev is not None and self.facing == prev.facing and not self.is_faster_than(prev):
            return False
        
        dist_to_next = self._rel_grid.calc_dist_to_next(RelativePosition.left(1))
        return dist_to_next is None or dist_to_next > self._vel
    
    def can_move_right(self) -> bool:
        if not self._rel_grid.is_inbounds(RelativePosition.right(1)):
            return False
        
        if self._rel_grid.is_fill(RelativePosition.right(1)):
            return False
        
        prev = self._rel_grid.get_prev(RelativePosition.right(1),
                                       lambda obj: obj.facing == self.facing)
        if prev is not None and self.facing == prev.facing and not self.is_faster_than(prev):
            return False
        
        dist_to_next = self._rel_grid.calc_dist_to_next(RelativePosition.right(1))
        return dist_to_next is None or dist_to_next > self._vel
    
    def is_faster_than(self, other: 'Pedestrian') -> bool:
        return self._vel > other._vel
    
    def _get_pos_forward(self) -> RelativePosition:
        dist_to_next = self._rel_grid.calc_dist_to_next(RelativePosition.still(),
                                                        lambda obj: obj.facing != opposite_direction(self.facing))
        if dist_to_next is None or dist_to_next > self._vel:
            return RelativePosition.forward(self._vel)
        return RelativePosition.forward(dist_to_next)
    
    def _get_pos_left_right_random(self) -> RelativePosition:
        p = gen.random()
        if p > 0.5:
            return RelativePosition.left(1)
        else:
            return RelativePosition.right(1)

    def think(self, crosswalk_zone: Rectangle, pedestrian_stop_light: StopLight = None):
        if pedestrian_stop_light.is_red() and not self._rel_grid.is_in(crosswalk_zone):
            self._desired_displacement = RelativePosition.still()
            return
        
        if pedestrian_stop_light is not None and pedestrian_stop_light.is_red():
            self._vel = 6
            self._repr = "😰"

        if self.can_move_forward():
            self._desired_displacement = self._get_pos_forward()
        else:
            can_move_left = self.can_move_left()
            can_move_right = self.can_move_right()
            
            if can_move_left and not can_move_right:
                self._desired_displacement = RelativePosition.left(1)
            elif can_move_right and not can_move_left:
                self._desired_displacement = RelativePosition.right(1)
            elif can_move_left and can_move_right:
                self._desired_displacement = self._get_pos_left_right_random()
            else:
                self._desired_displacement = RelativePosition.still()

    def move(self, _: Rectangle):
        if not self._rel_grid.is_inbounds(self._desired_displacement):
            self._rel_grid.clear()
            return
        self._rel_grid.move(self._desired_displacement)