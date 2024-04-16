from typing import Tuple

from grid import Direction
from relative_grid import RelativeGrid
from generator.tp_generator import TPGenerator
from movements import Forward, Still, TurnLeft, TurnRight, NoTurn, TurnMovement
from semaphore import Semaphore

from orientable import Orientable

gen = TPGenerator(4*10**7)

class Pedestrian(Orientable):
    def __init__(self, rel_grid: RelativeGrid, velocity: int = None, repr: str = None):
        self._desired_movement = None
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
        return not self._rel_grid.is_fill(Forward(1))
    
    def can_move_left(self) -> bool:
        if not self._rel_grid.is_inbounds(TurnLeft(1)):
            return False
        
        if self._rel_grid.is_fill(TurnLeft(1)):
            return False
        
        prev = self._rel_grid.get_prev(TurnLeft(1))
        if prev is not None and self.facing == prev.facing and not self.is_faster_than(prev):
            return False
        
        dist_to_next = self._rel_grid.calc_dist_to_next(TurnLeft(1))
        return dist_to_next is None or dist_to_next > self._vel
    
    def can_move_right(self) -> bool:
        if not self._rel_grid.is_inbounds(TurnRight(1)):
            return False
        
        if self._rel_grid.is_fill(TurnRight(1)):
            return False
        
        prev = self._rel_grid.get_prev(TurnRight(1))
        if prev is not None and self.facing == prev.facing and not self.is_faster_than(prev):
            return False
        
        dist_to_next = self._rel_grid.calc_dist_to_next(TurnRight(1))
        return dist_to_next is None or dist_to_next > self._vel
    
    def is_faster_than(self, other: 'Pedestrian') -> bool:
        return self._vel > other._vel
    
    def _get_pos_forward(self) -> Forward:
        dist_to_next = self._rel_grid.calc_dist_to_next(Still())
        if dist_to_next is None or dist_to_next > self._vel:
            return Forward(self._vel)
        return Forward(dist_to_next)
    
    def _get_pos_left_right_random(self) -> TurnMovement:
        p = gen.random()
        if p > 0.5:
            return TurnLeft(1)
        else:
            return TurnRight(1)

    def think(self, pedestrian_sem: Semaphore = None):
        if pedestrian_sem is not None and pedestrian_sem.state == "red":
            self._vel = 6
            self._repr = "😰"

        if self.can_move_forward():
            self._desired_movement = self._get_pos_forward()
        else:
            can_move_left = self.can_move_left()
            can_move_right = self.can_move_right()
            
            if can_move_left and not can_move_right:
                self._desired_movement = TurnLeft(1)
            elif can_move_right and not can_move_left:
                self._desired_movement = TurnRight(1)
            elif can_move_left and can_move_right:
                self._desired_movement = self._get_pos_left_right_random()
            else:
                self._desired_movement = Still()

    def move(self):
        self._rel_grid.move(self._desired_movement)