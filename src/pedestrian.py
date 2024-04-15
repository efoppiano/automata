from typing import Tuple

from grid import Direction
from relative_grid import RelativeGrid
from generator.tp_generator import TPGenerator
from movements import Forward, Still, TurnLeft, TurnRight, NoTurn, TurnMovement

gen = TPGenerator(4*10**7)

class Pedestrian:
    def __init__(self, facing: Direction, velocity: int = None):
        self._facing = facing
        self._desired_movement = None

        if velocity is not None:
            self._vel = velocity
        else:
            self._vel = self._generate_velocity()

    @property
    def facing(self) -> Direction:
        return self._facing
    
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

    def can_move_forward(self, rel_grid: RelativeGrid) -> bool:
        return not rel_grid.is_fill(Forward(1), NoTurn())
    
    def can_move_left(self, rel_grid: RelativeGrid) -> bool:
        if not rel_grid.is_inbounds(Still(), TurnLeft(1)):
            return False
        
        if rel_grid.is_fill(Still(), TurnLeft(1)):
            return False
        
        prev = rel_grid.get_prev(Still(), TurnLeft(1))
        if prev is not None and self.facing == prev.facing and not self.is_faster_than(prev):
            return False
        
        dist_to_next = rel_grid.calc_dist_to_next(Still(), TurnLeft(1))
        return dist_to_next is None or dist_to_next > self._vel
    
    def can_move_right(self, rel_grid: RelativeGrid) -> bool:
        if not rel_grid.is_inbounds(Still(), TurnRight(1)):
            return False
        
        if rel_grid.is_fill(Still(), TurnRight(1)):
            return False
        
        prev = rel_grid.get_prev(Still(), TurnRight(1))
        if prev is not None and self.facing == prev.facing and not self.is_faster_than(prev):
            return False
        
        dist_to_next = rel_grid.calc_dist_to_next(Still(), TurnRight(1))
        return dist_to_next is None or dist_to_next > self._vel
    
    def is_faster_than(self, other: 'Pedestrian') -> bool:
        return self._vel > other._vel
    
    def _get_pos_forward(self, rel_grid: RelativeGrid) -> Forward:
        dist_to_next = rel_grid.calc_dist_to_next(Still(), NoTurn())
        if dist_to_next is None or dist_to_next > self._vel:
            return Forward(self._vel)
        return Forward(dist_to_next)
    
    def _get_pos_left_right_random(self) -> TurnMovement:
        p = gen.random()
        if p > 0.5:
            return TurnLeft(1)
        else:
            return TurnRight(1)

    def think(self, rel_grid: RelativeGrid):
        if self.can_move_forward(rel_grid):
            self._desired_movement = self._get_pos_forward(rel_grid)
        else:
            can_move_left = self.can_move_left(rel_grid)
            can_move_right = self.can_move_right(rel_grid)
            
            if can_move_left and not can_move_right:
                self._desired_movement = TurnLeft(1)
            elif can_move_right and not can_move_left:
                self._desired_movement = TurnRight(1)
            elif can_move_left and can_move_right:
                self._desired_movement = self._get_pos_left_right_random()
            else:
                self._desired_movement = Still()

                
