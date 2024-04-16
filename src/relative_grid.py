from typing import Tuple, TypeVar, Generic, Optional

from grid import Direction, Grid, CellAlreadyFill

from movements import StraightMovement, TurnMovement, Movement, Still, NoTurn

from generator.tp_generator import TPGenerator

T = TypeVar("T")

gen = TPGenerator(3**10**7)

class RelativeGrid(Generic[T]):
    def __init__(self, center: Tuple[int, int], facing: Direction, grid: Grid[T]):
        self._center = center
        self._facing = facing
        self._grid = grid

    @property
    def facing(self) -> Direction:
        return self._facing
    
    def spawn(self, obj: T) -> bool:
        if self.facing == "East":
            return self._spawn_facing_east(obj)
        else:
            return self._spawn_facing_west(obj)

    def _spawn_facing_east(self, obj: T) -> bool:
        if self._grid.is_column_full(0):
            return False

        while True:
            possible_pos = gen.randint(0, self._grid.width)
            if not self._grid.is_fill(possible_pos, 0):
                self._grid.fill(possible_pos, 0, obj)
                return True
            
    def _spawn_facing_west(self, obj: T) -> bool:
        if self._grid.is_column_full(self._grid.length-1):
            return False

        while True:
            possible_pos = gen.randint(0, self._grid.width)
            if not self._grid.is_fill(possible_pos, self._grid.length-1):
                self._grid.fill(possible_pos, self._grid.length-1, obj)
                return True


    def is_fill(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> bool:
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        if self._grid.is_fill(row, col):
            facing = self._grid.get_value(row, col).facing
            return facing == self._facing
        return False
    
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
        
    def calc_dist_to_next(self, straight_mov: StraightMovement, turn_mov: TurnMovement) -> Optional[int]:
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        if self._facing == "East":
            next_val = self._grid.get_next(row, col)
            if next_val is None:
                return None
            if next_val.facing == self._facing:
                return self._grid.calc_dist_to_next(row, col)
            
            dist = self._grid.calc_dist_to_next(row, col)
            dist_to_next_next = self.calc_dist_to_next(straight_mov + dist + 1, turn_mov)
            if dist_to_next_next is None:
                return None
            return dist + dist_to_next_next
        else:
            prev_val = self._grid.get_prev(row, col)
            if prev_val is None:
                return None
            
            if prev_val.facing == self._facing:
                return self._grid.calc_dist_to_prev(row, col)
            
            dist = self._grid.calc_dist_to_prev(row, col)

            dist_to_prev_prev = self.calc_dist_to_next(straight_mov + dist + 1, turn_mov)
            

            if dist_to_prev_prev is None:
                return None
            return dist + dist_to_prev_prev

    def move(self, movement: Movement):
        if movement == Still() or movement == NoTurn():
            return
        
        if isinstance(movement, StraightMovement):
            straight_mov = movement
            turn_mov = NoTurn()
        
        if isinstance(movement, TurnMovement):
            straight_mov = movement
            turn_mov = movement
        
        if not self.is_fill(Still(), NoTurn()):
            raise Exception("Attempted to move an empty cell")
        
        if not self.is_inbounds(straight_mov, turn_mov):
            self._grid.pedestrian_passed(self._facing)
            self._grid.clear(self._center[0], self._center[1])
            return

        
        if self.is_fill(straight_mov, turn_mov):
            raise CellAlreadyFill(*self._get_abs_pos(straight_mov, turn_mov))
        
        me = self._grid.get_value(self._center[0], self._center[1])
        row, col = self._get_abs_pos(straight_mov, turn_mov)
        try:
            self._grid.fill(row, col, me)
        except CellAlreadyFill:
            return self.move(movement - 1)

        self._grid.clear(self._center[0], self._center[1])