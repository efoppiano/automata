from typing import Tuple

RowNumber = int
ColNumber = int
Point = Tuple[RowNumber, ColNumber]

class Rectangle:
    def __init__(self, rows: int, cols: int):
        self._upper_left: Point = (0, 0)
        self._lower_right: Point = (rows - 1, cols - 1)

    @classmethod
    def _new_with_points(cls, upper_left: Point, lower_right: Point):
        new_rect = Rectangle(0, 0)
        new_rect._upper_left = (upper_left[0], upper_left[1])
        new_rect._lower_right = (lower_right[0], lower_right[1])
        return new_rect
    
    def is_inside(self, point: Point) -> bool:
        x, y = point
        x1, y1 = self._upper_left
        x2, y2 = self._lower_right
        return x1 <= x <= x2 and y1 <= y <= y2
    
    def __repr__(self) -> str:
        return f"Rectangle({self._upper_left}, {self._lower_right})"
    
    @property
    def start_col(self) -> int:
        return self._upper_left[1]
    
    @property
    def start_row(self) -> int:
        return self._upper_left[0]
    
    @property
    def end_col(self) -> int:
        return self._lower_right[1]
    
    @property
    def end_row(self) -> int:
        return self._lower_right[0]
    
    @property
    def cols(self) -> int:
        return self.end_col - self.start_col + 1
    
    @property
    def rows(self) -> int:
        return self.end_row - self.start_row + 1
    
    @property
    def upper_left(self) -> Point:
        return self._upper_left
    
    @property
    def upper_right(self) -> Point:
        return (self._upper_left[0], self._lower_right[1])
    
    @property
    def lower_right(self) -> Point:
        return self._lower_right
    
    @property
    def lower_left(self) -> Point:
        return (self._lower_right[0], self._upper_left[1])
    

    def move_up(self, rows: int):
        self._upper_left = (self._upper_left[0] - rows, self._upper_left[1])
        self._lower_right = (self._lower_right[0] - rows, self._lower_right[1])

    def move_down(self, rows: int):
        return self.move_up(-rows)
    
    def move_left(self, cols: int):
        self._upper_left = (self._upper_left[0], self._upper_left[1] - cols)
        self._lower_right = (self._lower_right[0], self._lower_right[1] - cols)

    def move_right(self, cols: int):
        return self.move_left(-cols)
    
    def duplicate(self):
        return Rectangle._new_with_points(self._upper_left, self._lower_right)
    
    def distance_to(self, point: Point) -> int:
        row, col = point

        if self.start_row <= row <= self.end_row:
            return min(abs(self.start_col - col), abs(self.end_col - col)) - 1
        if self.start_col <= col <= self.end_col:
            return min(abs(self.start_row - row), abs(self.end_row - row)) - 1
        raise ValueError(f"Cannot calculate distance to point {point} from rectangle {self}")