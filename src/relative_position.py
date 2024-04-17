from typing import Tuple

from directions import Direction

class RelativePosition:
    def __init__(self, forward: int, right: int):
        self._forward = forward
        self._right = right

    def __repr__(self) -> str:
        return f"RelativePosition({self._forward}, {self._right})"

    def is_still(self) -> bool:
        return self._forward == 0 and self._right == 0
    
    def decrease(self):
        if self._forward > 0:
            self._forward -= 1
        elif self._forward < 0:
            self._forward += 1
        if self._right > 0:
            self._right -= 1
        elif self._right < 0:
            self._right += 1
    
    @classmethod
    def forward(cls, amount: int) -> "RelativePosition":
        return cls(amount, 0)
    
    @classmethod
    def backward(cls, amount: int) -> "RelativePosition":
        return cls(-amount, 0)
    
    @classmethod
    def right(cls, amount: int) -> "RelativePosition":
        return cls(0, amount)
    
    @classmethod
    def left(cls, amount: int) -> "RelativePosition":
        return cls(0, -amount)

    @classmethod
    def still(cls) -> "RelativePosition":
        return cls(0, 0)

    def __add__(self, other: "RelativePosition") -> "RelativePosition":
        return type(self)(self._forward + other._forward, self._right + other._right)

    def apply(self, facing: Direction, center: Tuple[int, int]) -> Tuple[int, int]:
        if facing == "East":
            return center[0] + self._right, center[1] + self._forward
        elif facing == "West":
            return center[0] - self._right, center[1] - self._forward
        elif facing == "North":
            return center[0] - self._forward, center[1] + self._right
        elif facing == "South":
            return center[0] + self._forward, center[1] - self._right
        else:
            raise Exception(f"Invalid direction {facing}")