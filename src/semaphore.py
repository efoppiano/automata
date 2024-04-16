
from typing import Literal

SemaphoreState = Literal["red", "green"]

class Semaphore:
    def __init__(self, cycle: int, green_light_time: int, initial_state: SemaphoreState = "green"):
        assert green_light_time < cycle

        self._cycle = cycle
        self._green_light_time = green_light_time
        self._time_to_change = green_light_time
        self._state = initial_state

    def update(self):
        self._time_to_change -= 1
        if self._time_to_change == 0:
            self._state = "green" if self._state == "red" else "red"
            self._time_to_change = self._green_light_time if self._state == "green" else self._cycle - self._green_light_time

    @property
    def state(self) -> SemaphoreState:
        return self._state

    
    def show(self):
        if self._state == "green":
            print("🟢", self._time_to_change)
        else:
            print("🔴", self._time_to_change)