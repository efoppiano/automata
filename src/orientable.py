from abc import ABC, abstractmethod

from directions import Direction

class Orientable(ABC):
    @property
    @abstractmethod
    def facing(self) -> Direction:
        pass
