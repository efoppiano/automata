from abc import ABC, abstractmethod

class Generator(ABC):
    @abstractmethod
    def random(self) -> float:
        pass

    @abstractmethod
    def randint(self, a: int, b: int) -> int:
        pass

    @abstractmethod
    def poi(self, l: float) -> int:
        pass