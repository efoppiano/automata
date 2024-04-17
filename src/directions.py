from typing import Literal

Direction = Literal["East", "West", "North", "South"]

def opposite_direction(direction: Direction) -> Direction:
    if direction == "East":
        return "West"
    elif direction == "West":
        return "East"
    elif direction == "North":
        return "South"
    else:
        return "North"