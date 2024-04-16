from typing import Tuple

from grid import Grid, CellAlreadyFill
from relative_grid import RelativeGrid
from pedestrian import Pedestrian
from waiting_area import WaitingArea
from generator.tp_generator import TPGenerator

gen = TPGenerator(9*10**7)

class Automata:
    def __init__(self, rows: int, cols: int):
        self._grid = Grid[Pedestrian](rows, cols)
        self._waiting_area_west = WaitingArea(500/360, RelativeGrid((0, 0), "East", self._grid))
        self._waiting_area_east = WaitingArea(500/360, RelativeGrid((rows-1, cols-1), "West", self._grid))
        self._moved_pedestrians = set()

    def update(self):
        self._waiting_area_east.update()
        self._waiting_area_west.update()
        if gen.random() > 0.5:
            self._grid.apply(lambda pedestrian, pos: pedestrian.think(RelativeGrid(pos, pedestrian.facing, self._grid)))
        else:
            self._grid.apply_rev(lambda pedestrian, pos: pedestrian.think(RelativeGrid(pos, pedestrian.facing, self._grid)))
        
        self._grid.apply(self.move_pedestrian)
        self._moved_pedestrians.clear()

    def move_pedestrian(self, pedestrian: Pedestrian, center: Tuple[int, int]):
        if pedestrian in self._moved_pedestrians:
            return
        try:
            RelativeGrid(center, pedestrian.facing, self._grid).move(pedestrian._desired_movement)
        except CellAlreadyFill:
            pass
        self._moved_pedestrians.add(pedestrian)

    def show(self):
        self._grid.show()

