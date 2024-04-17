from typing import Tuple

from grid import Grid, CellAlreadyFill
from relative_grid import RelativeGrid
from rectangle import Rectangle
from pedestrian import Pedestrian
from waiting_area import WaitingArea
from generator.tp_generator import TPGenerator
from semaphore import Semaphore

gen = TPGenerator(9*10**7)

class Automata:
    def __init__(self, rows: int, cols: int):
        waiting_area_length = 5
        total_rows = rows
        total_cols = cols + 2*waiting_area_length
        self._grid = Grid[Pedestrian](total_rows, total_cols)
        self._pedestrian_sem = Semaphore(20, 10)
        pedesrian_zone = Rectangle((0, waiting_area_length), (total_rows-1, total_cols-1-waiting_area_length))

        grid_area_west = RelativeGrid((0, waiting_area_length), pedesrian_zone, "East", self._grid)
        grid_area_east = RelativeGrid((total_rows-1, total_cols-1-waiting_area_length), pedesrian_zone, "West", self._grid)

        self._waiting_area_west = WaitingArea(500/360, grid_area_west, self._pedestrian_sem)
        self._waiting_area_east = WaitingArea(500/360, grid_area_east, self._pedestrian_sem)
        
        self._moved_pedestrians = set()

    def update(self):
        self._pedestrian_sem.update()
        self._waiting_area_east.update()
        self._waiting_area_west.update()
        # self.show()
        self._grid.apply(lambda pedestrian, _: pedestrian.think(self._pedestrian_sem))
        
        self._grid.apply(self.move_pedestrian)
        
        self._moved_pedestrians.clear()

    def move_pedestrian(self, pedestrian: Pedestrian, _: Tuple[int, int]):
        if pedestrian in self._moved_pedestrians:
            return
        try:
            pedestrian.move()
        except CellAlreadyFill:
            pass
        self._moved_pedestrians.add(pedestrian)

    def show(self):
        self._pedestrian_sem.show()
        print("Waiting at East:", self._waiting_area_east)
        print("Waiting at West:", self._waiting_area_west)
        
        self._grid.show()

