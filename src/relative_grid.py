from typing import Tuple, TypeVar, Generic, Optional

from grid import Direction, Grid

from movements import StraightMovement, TurnMovement

T = TypeVar("T")

class RelativeGrid(Generic[T]):
    def __init__(self, center: Tuple[int, int], facing: Direction, grid: Grid[T]):
        self._center = center
        self._facing = facing
        self._grid = grid

    def is_fill(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> bool:
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        return self._grid.is_fill(row, col)
    
    def _get_abs_pos(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> Tuple[int, int]:
        if self._facing == "East":
            return self._center[0] + turn_mov, self._center[1] + straight_mov
        elif self._facing == "West":
            return self._center[0] - turn_mov, self._center[1] - straight_mov
        
    def is_inbounds(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> bool:
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        return 0 <= row < self._grid.width and 0 <= col < self._grid.length

    def get_prev(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> Optional[T]:
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        if self._facing == "East":
            return self._grid.get_prev(row, col)
        else:
            return self._grid.get_next(row, col)
        
    def get_next(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> Optional[T]:
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        if self._facing == "East":
            return self._grid.get_next(straight_mov, turn_mov)
        else:
            return self._grid.get_prev(straight_mov, turn_mov)
        
    def calc_dist_to_next(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> int:
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        if self._facing == "East":
            return self._grid.calc_dist_to_next(row, col)
        else:
            return self._grid.calc_dist_to_prev(row, col)