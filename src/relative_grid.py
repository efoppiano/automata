from typing import Tuple, TypeVar, Generic, Optional, Callable

from grid import Grid, CellAlreadyFill

from movements import StraightMovement, TurnMovement, Movement, Still, NoTurn

from generator.tp_generator import TPGenerator

from directions import Direction, opposite_direction

from orientable import Orientable

T = TypeVar("T", bound=Orientable)

gen = TPGenerator(3**10**7)

class RelativeGrid(Generic[T]):
    def __init__(self, center: Tuple[int, int], facing: Direction, grid: Grid[T]):
        self._center = center
        self._facing = facing
        self._grid = grid

    @property
    def facing(self) -> Direction:
        return self._facing
    
    def spawn(self, f: Callable[['RelativeGrid'], T]) -> bool:
        if self.facing == "East":
            return self._spawn_facing_east(f)
        else:
            return self._spawn_facing_west(f)

    def _spawn_facing_east(self, f: Callable[['RelativeGrid'], T]) -> bool:
        if self._grid.is_column_full(0):
            return False

        while True:
            possible_pos = gen.randint(0, self._grid.width)
            if not self._grid.is_fill(possible_pos, 0):
                obj = f(RelativeGrid((possible_pos, 0), self._facing, self._grid))
                self._grid.fill(possible_pos, 0, obj)
                return True
            
    def _spawn_facing_west(self, f: Callable[['RelativeGrid'], T]) -> bool:
        if self._grid.is_column_full(self._grid.length-1):
            return False

        while True:
            possible_pos = gen.randint(0, self._grid.width)
            if not self._grid.is_fill(possible_pos, self._grid.length-1):
                obj = f(RelativeGrid((possible_pos, self._grid.length-1), self._facing, self._grid))
                self._grid.fill(possible_pos, self._grid.length-1, obj)
                return True


    def is_fill(self, movement: Movement) -> bool:
        row, col = movement.apply(self._facing, self._center)
        if self._grid.is_fill(row, col):
            facing = self._grid.get_value(row, col).facing
            if self._facing == opposite_direction(facing):
                return False
            return True            
        return False
    
    def is_inbounds(self, movement: Movement) -> bool:
        row, col = movement.apply(self._facing, self._center)
        return 0 <= row < self._grid.width and 0 <= col < self._grid.length

    def get_prev(self, movement: Movement) -> Optional[T]:
        row, col = movement.apply(self._facing, self._center)
        if self._facing == "East":
            return self._grid.get_prev(row, col)
        else:
            return self._grid.get_next(row, col)
        
    def get_next(self, movement: Movement) -> Optional[T]:
        row, col = movement.apply(self._facing, self._center)
        if self._facing == "East":
            return self._grid.get_next(row, col)
        else:
            return self._grid.get_prev(row, col)
        
    def calc_dist_to_next(self, movement: Movement) -> Optional[int]:
        row, col = movement.apply(self._facing, self._center)
        if self._facing == "East":
            return self._grid.calc_dist_to_next(row, col, lambda elem: elem.facing == self._facing)
        else:
            return self._grid.calc_dist_to_prev(row, col, lambda elem: elem.facing == self._facing)

    def move(self, movement: Movement):
        if movement == Still():
            return
        
        if not self.is_fill(Still()):
            raise Exception("Attempted to move an empty cell")
        
        if not self.is_inbounds(movement):
            self._grid.pedestrian_passed(self._facing)
            self._grid.clear(self._center[0], self._center[1])
            return

        
        if self.is_fill(movement):
            raise CellAlreadyFill(*movement.apply(self._facing, self._center))
        
        me = self._grid.get_value(self._center[0], self._center[1])
        row, col = movement.apply(self._facing, self._center)
        try:
            self._grid.fill(row, col, me)
        except CellAlreadyFill:
            return self.move(movement - 1)

        self._grid.clear(self._center[0], self._center[1])
        self._center = (row, col)
