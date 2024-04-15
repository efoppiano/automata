from typing import Union, Literal, TypeVar, Generic, Optional

from generator.tp_generator import TPGenerator

gen = TPGenerator(4*10**7)

Direction = Literal["East", "West"]

T = TypeVar("T")

class Grid(Generic[T]):
    def __init__(self, width: int, length: int):
        self._grid = [[None for i in range(length)] for j in range(width)]

    def is_fill(self, row: int, col: int) -> bool:
        if row < 0 or row >= self.width:
            raise Exception(f"Row {row} out of bounds")
        if col < 0 or col >= self.length:
            return False
        
        return self._grid[row][col] is not None

    def fill(self, row: int, col: int, v: T):
        if self.is_fill(row, col):
            raise Exception(f"Attempted to fill an already fill cell ({row}, {col})")
            
        self._grid[row][col] = v

    def get_value(self, row: int, col: int) -> T:
        if not self.is_fill(row, col):
            raise Exception(f"Element not found at row {row}, col {col}")
        return self._grid[row][col]

    @property
    def width(self):
        return len(self._grid)

    @property
    def length(self):
        return len(self._grid[0])

    def calc_dist_to_next(self, row: int, col: int) -> Optional[int]:
        for i in range(col+1, self.length):
            if self.is_fill(row, i):
                return i - col - 1
        return None
    
    def calc_dist_to_prev(self, row: int, col: int) -> Optional[int]:
        for i in range(col-1, -1, -1):
            if self.is_fill(row, i):
                return col - i - 1
        return None
    
    def get_prev(self, row: int, col: int) -> Optional[T]:
        dist = self.calc_dist_to_prev(row, col)
        if dist is None:
            return None
        return self.get_value(row, col - dist - 1)
    
    def get_next(self, row: int, col: int) -> Optional[T]:
        dist = self.calc_dist_to_next(row, col)
        if dist is None:
            return None
        return self.get_value(row, col + dist + 1)