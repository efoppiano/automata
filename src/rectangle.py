from typing import Tuple

Point = Tuple[int, int]

class Rectangle:
    def __init__(self, length: int, width: int):
        self._upper_left = (0, 0)
        self._lower_right = (width - 1, length - 1)

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
    

    def move_left(self, amount: int):
        self._upper_left = (self._upper_left[0], self._upper_left[1] - amount)
        self._lower_right = (self._lower_right[0], self._lower_right[1] - amount)

    def move_right(self, amount: int):
        return self.move_left(-amount)
    
    def move_up(self, amount: int):
        self._upper_left = (self._upper_left[0] - amount, self._upper_left[1])
        self._lower_right = (self._lower_right[0] - amount, self._lower_right[1])

    def move_down(self, amount: int):
        return self.move_up(-amount)
    
    def duplicate(self):
        return Rectangle(self.length, self.width)