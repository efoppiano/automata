from abc import ABC, abstractmethod

class Movement(ABC):
    @abstractmethod
    def __add__(self, other) -> int:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    def __radd__(self, other) -> int:
        return self.__add__(other)
    
    def __sub__(self, other) -> int:
        return self.__add__(-other)

    def __rsub__(self, other) -> int:
        return -self.__sub__(other)

class StraightMovement(Movement):
    pass

class Forward(StraightMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __add__(self, other) -> int:
        return self._amount + other
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "Forward" and self._amount == other._amount
    
class Backward(StraightMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __add__(self, other) -> int:
        return -self._amount + other
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "Backward" and self._amount == other._amount
    
class Still(StraightMovement):
    def __add__(self, other) -> int:
        return 0 + other
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "Still"
    
class TurnMovement(Movement):
    pass

class TurnLeft(TurnMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __add__(self, other) -> int:
        return -self._amount + other
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "TurnLeft" and self._amount == other._amount
    
class TurnRight(TurnMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __add__(self, other) -> int:
        return self._amount + other
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "TurnRight" and self._amount == other._amount
    
class NoTurn(TurnMovement):
    def __add__(self, other) -> int:
        return 0 + other
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "NoTurn"