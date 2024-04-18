from typing import Tuple, TypeVar, Generic, Optional, Callable

from grid import Grid, CellAlreadyFill

from generator.tp_generator import TPGenerator

from directions import Direction, opposite_direction
from relative_position import RelativePosition
from rectangle import Point, Rectangle
from orientable import Orientable

T = TypeVar("T", bound=Orientable)

gen = TPGenerator(3**10**7)

class RelativeGrid(Generic[T]):
    def __init__(self, center: Point, bounds: Rectangle, facing: Direction, grid: Grid[T]):
        self._center = center
        self._bounds = bounds
        self._facing = facing
        self._grid = grid

    def new_displaced(self, displacement: RelativePosition) -> 'RelativeGrid':
        new_center = displacement.apply(self._facing, self._center)
        return self.__class__(new_center, self._bounds, self._facing, self._grid)
    
    @property
    def facing(self) -> Direction:
        return self._facing
    
    @property
    def width(self) -> int:
        return self._bounds.width
    
    @property
    def length(self) -> int:
        return self._bounds.length
    
    def is_in(self, zone: Rectangle) -> bool:
        return zone.is_inside(self._center)
    
    def fill(self, displacement: RelativePosition, obj: T):
        if not self.is_inbounds(displacement):
            raise Exception(f"Attempted to fill an out of bounds cell {displacement.apply(self._facing, self._center)} - Bounds: {self._bounds}")

        row, col = displacement.apply(self.facing, self._center)
        self._grid.fill(row, col, obj)

    def is_fill(self, displacement: RelativePosition, ignore_opposite_direction: bool = True) -> bool:
        if not self.is_inbounds(displacement):
            return False
        
        row, col = displacement.apply(self.facing, self._center)
        if self._grid.is_fill(row, col):
            if not ignore_opposite_direction:
                return True
            return self._grid.get_value(row, col).facing != opposite_direction(self.facing)
        return False
    
    def is_inbounds(self, displacement: RelativePosition = RelativePosition.still()) -> bool:
        row, col = displacement.apply(self._facing, self._center)
        if not self._bounds.is_inside((row, col)):
            return False

        return 0 <= row < self._grid.width and 0 <= col < self._grid.length

    def get_prev(self, displacement: RelativePosition, f: Callable[[T], bool] = None) -> Optional[T]:
        if f is None:
            f = lambda _: True

        row, col = displacement.apply(self._facing, self._center)
        if self._facing == "East":
            return self._grid.get_prev(row, col, f)
        elif self._facing == "West":
            return self._grid.get_next(row, col, f)
        elif self._facing == "North":
            return self._grid.get_vertically_next(row, col, f)
        elif self._facing == "South":
            return self._grid.get_vertically_prev(row, col, f)
        
    def get_next(self, displacement: RelativePosition, f: Callable[[T], bool] = None) -> Optional[T]:
        if f is None:
            f = lambda _: True

        row, col = displacement.apply(self._facing, self._center)
        if self._facing == "East":
            return self._grid.get_next(row, col, f)
        elif self._facing == "West":
            return self._grid.get_prev(row, col, f)
        elif self._facing == "North":
            return self._grid.get_vertically_prev(row, col, f)
        elif self._facing == "South":
            return self._grid.get_vertically_next(row, col, f)
        
        
    def calc_dist_to_next(self, displacement: RelativePosition, f: Callable[[T], bool] = None) -> Optional[int]:
        if f is None:
            f = lambda _: True
        row, col = displacement.apply(self._facing, self._center)
        if self._facing == "East":
            return self._grid.calc_dist_to_next(row, col, f)
        elif self._facing == "West":
            return self._grid.calc_dist_to_prev(row, col, f)
        elif self._facing == "North":
            return self._grid.calc_dist_to_vertically_prev(row, col, f)
        elif self._facing == "South":
            return self._grid.calc_dist_to_vertically_next(row, col, f)
        
    def calc_dist_to_zone(self, displacement: RelativePosition, zone: Rectangle) -> Optional[int]:
        row, col = displacement.apply(self._facing, self._center)
        return zone.distance_to((row, col))

    def clear(self, displacement: RelativePosition = RelativePosition.still()):
        row, col = displacement.apply(self._facing, self._center)
        self._grid.clear(row, col)

    def move(self, displacement: RelativePosition):
        if displacement.is_still():
            return
        
        if not self.is_fill(RelativePosition.still(), ignore_opposite_direction=False):
            raise Exception(f"Attempted to move an empty cell ({self._center[0]}, {self._center[1]})")
        
        if not self.is_inbounds(displacement):
            raise Exception(f"Attempted to move out of bounds cell {displacement.apply(self._facing, self._center)} - Bounds: {self._bounds}")

        
        if self.is_fill(displacement):
            raise CellAlreadyFill(*displacement.apply(self._facing, self._center))
        
        me = self._grid.get_value(self._center[0], self._center[1])
        row, col = displacement.apply(self._facing, self._center)
        try:
            self._grid.fill(row, col, me)
        except CellAlreadyFill:
            displacement.decrease()
            return self.move(displacement)

        self._grid.clear(self._center[0], self._center[1])
        self._center = (row, col)
