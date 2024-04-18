
from typing import Literal

StopLightState = Literal["red", "green", "yellow"]

class StopLight:
    def __init__(self, cycle: int, green_light_time: int, yellow_light_time: int):
        assert green_light_time + yellow_light_time < cycle

        self._cycle = cycle
        self._green_light_time = green_light_time
        self._yellow_light_time = yellow_light_time
        self._red_light_time = cycle - green_light_time - yellow_light_time
        self._time_to_change = self._green_light_time
        self._state = "green"
        self._prev_state = "yellow"

    def _get_next_state(self) -> StopLightState:
        if self._state == "green" or self._state == "red":
            return "yellow"
        if self._state == "yellow" and self._prev_state == "green":
            return "red"
        return "green"

    def _get_next_time_to_change(self, new_state: StopLightState) -> int:
        if new_state == "green":
            return self._green_light_time
        if new_state == "yellow":
            return self._yellow_light_time
        return self._red_light_time

    def update(self):
        self._time_to_change -= 1
        if self._time_to_change == 0:
            new_state = self._get_next_state()
            next_time_to_change = self._get_next_time_to_change(new_state)
            self._prev_state = self._state
            self._state = new_state
            self._time_to_change = next_time_to_change

    @property
    def state(self) -> StopLightState:
        return self._state

    def is_green(self) -> bool:
        return self._state == "green"
    
    def is_red(self) -> bool:
        return self._state == "red"
    
    def is_yellow(self) -> bool:
        return self._state == "yellow"

    def show(self):
        if self._state == "green":
            print("🟢", self._time_to_change)
        elif self._state == "yellow":
            print("🟡", self._time_to_change)
        else:
            print("🔴", self._time_to_change)