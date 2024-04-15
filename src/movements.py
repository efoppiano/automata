from abc import ABC, abstractmethod

class Movement(ABC):
    @abstractmethod
    def __add__(self, other) -> 'Movement':
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __radd__(self, other) -> int:
        pass

    @abstractmethod
    def __neg__(self) -> 'Movement':
        pass
    
    def __sub__(self, other) -> 'Movement':
        return self.__add__(-other)

    def __rsub__(self, other) -> int:
        return -(-other + self)

    
    @abstractmethod
    def __repr__(self) -> str:
        pass

class StraightMovement(Movement):
    pass

class Forward(StraightMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._amount})"

    def __add__(self, other) -> 'Movement':
        self._amount += other
        if self._amount == 0:
            return Still()
        if self._amount < 0:
            return Backward(-self._amount)
        return self

    def __radd__(self, other) -> int:
        return self._amount + other

    def __neg__(self) -> 'Movement':
        return Backward(self._amount)
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "Forward" and self._amount == other._amount
    
class Backward(StraightMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._amount})"

    def __add__(self, other) -> 'Movement':
        self._amount += other
        if self._amount == 0:
            return Still()
        if self._amount < 0:
            return Forward(-self._amount)
        return self
    
    def __radd__(self, other) -> int:
        return -self._amount + other
    
    def __neg__(self) -> 'Movement':
        return Forward(self._amount)
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "Backward" and self._amount == other._amount
    
class Still(StraightMovement):
    def __repr__(self) -> str:
        return self.__class__.__name__
    
    def __add__(self, other) -> 'Movement':
        if other == 0:
            return self
        if other > 0:
            return Forward(other)
        return Backward(-other)
    
    def __radd__(self, other) -> int:
        return other
    
    def __neg__(self) -> 'Movement':
        return Still()
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "Still"
    
class TurnMovement(Movement):
    pass

class TurnLeft(TurnMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._amount})"

    def __add__(self, other) -> 'Movement':
        self._amount += other
        if self._amount == 0:
            return NoTurn()
        if self._amount < 0:
            return TurnRight(-self._amount)
        return self
    
    def __radd__(self, other) -> int:
        return -self._amount + other
    
    def __neg__(self) -> 'Movement':
        return TurnRight(self._amount)
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "TurnLeft" and self._amount == other._amount
    
class TurnRight(TurnMovement):
    def __init__(self, amount: int):
        self._amount = amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._amount})"

    def __add__(self, other) -> 'Movement':
        self._amount += other
        if self._amount == 0:
            return NoTurn()
        if self._amount < 0:
            return TurnLeft(-self._amount)
        return self
    
    def __radd__(self, other) -> int:
        return self._amount + other
    
    def __neg__(self) -> 'Movement':
        return TurnLeft(self._amount)
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "TurnRight" and self._amount == other._amount
    
class NoTurn(TurnMovement):
    def __repr__(self) -> str:
        return self.__class__.__name__
    
    def __add__(self, other) -> 'Movement':
        if other == 0:
            return self
        if other > 0:
            return TurnRight(other)
        return TurnLeft(-other)
    
    def __radd__(self, other) -> int:
        return other
    
    def __neg__(self) -> 'Movement':
        return NoTurn()
    
    def __eq__(self, other) -> bool:
        return other.__class__.__name__ == "NoTurn"