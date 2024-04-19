from abc import ABC, abstractmethod

from orientable import Orientable

class RoadEntity(Orientable, ABC):
    @abstractmethod
    def is_crossing(self) -> bool:
        pass
