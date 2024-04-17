from typing import Tuple

Point = Tuple[int, int]

class Rectangle:
    def __init__(self, upper_left: Point, lower_right: Point):
        self._upper_left = upper_left
        self._lower_right = lower_right

    def is_inside(self, point: Point) -> bool:
        x, y = point
        x1, y1 = self._upper_left
        x2, y2 = self._lower_right
        return x1 <= x <= x2 and y1 <= y <= y2
    
    def __repr__(self) -> str:
        return f"Rectangle({self._upper_left}, {self._lower_right})"
    
    @property
    def width(self) -> int:
        return self._lower_right[0] - self._upper_left[0] + 1
    
    @property
    def length(self) -> int:
        return self._lower_right[1] - self._upper_left[1] + 1