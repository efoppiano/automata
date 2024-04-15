from typing import Union, Literal, TypeVar, Generic, Optional

from generator.tp_generator import TPGenerator

gen = TPGenerator(4*10**7)

Direction = Literal["East", "West"]

T = TypeVar('T')

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

    def is_forward_fill(self, row: int, col: int, facing: Direction) -> bool:
        if facing == "East":
            return self.is_fill(row, col+1)
        else:
            return self.is_fill(row, col-1)

    def is_left_fill(self, row: int, col: int, facing: Direction) -> bool:
        if facing == "East":
            return self.is_fill(row-1, col)
        else:
            return self.is_fill(row+1, col)

    def is_right_fill(self, row: int, col: int, facing: Direction) -> bool:
        if facing == "East":
            return self.is_left_fill(row, col, "West")
        else:
            return self.is_left_fill(row, col, "East")

    def dist_to_next_value(self, row: int, col: int, facing: Direction) -> Optional[int]:
        if facing == "East":
            for i in range(col+1, self.length):
                if self.is_fill(row, i):
                    return i-col-1
            return None
        else:
            for i in range(col-1, 0, -1):
                if self.is_fill(row, i):
                    return col-i-1
            return None

    def get_prev_value_left(self, row: int, col: int, facing: Direction) -> Optional[T]:
        if facing == "East":
            dist = self.dist_to_next_value(row-1, col, "West")
            if dist is None:
                return None
            return self.get_value(row-1, col-dist-1)
        else:
            dist = self.dist_to_next_value(row+1, col, "East")
            if dist is None:
                return None
            return self.get_value(row+1, col+dist+1)
        
    def get_prev_value_right(self, row: int, col: int, facing: Direction) -> Optional[T]:
        if facing == "East":
            dist = self.dist_to_next_value(row+1, col, "West")
            if dist is None:
                return None
            print(dist)
            return self.get_value(row+1, col-dist-1)
        else:
            dist = self.dist_to_next_value(row-1, col, "East")
            if dist is None:
                return None
            return self.get_value(row-1, col+dist+1)