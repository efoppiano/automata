from typing import TypeVar, Generic, Optional, Callable, Tuple

from generator.tp_generator import TPGenerator
from directions import Direction

gen = TPGenerator(4*10**7)

CROSSWALK_START_ROW = 6
CROSSWALK_END_ROW = CROSSWALK_START_ROW+8

END_ROW = 19

class CellAlreadyFill(Exception):
    def __init__(self, row: int, col: int, v = None):
        self.row = row
        self.col = col
        if v is not None:
            super().__init__(f"Attempted to fill an already fill cell ({row}, {col}) containing {v}")
        else:
            super().__init__(f"Attempted to fill an already fill cell ({row}, {col})")

T = TypeVar("T")

class Grid(Generic[T]):
    def __init__(self, rows: int, cols: int):
        self._grid = [[None for i in range(cols)] for j in range(rows)]
        self._passed_to_west = 0
        self._passed_to_east = 0

    def is_fill(self, row: int, col: int) -> bool:
        if row < 0 or row >= self.rows:
            raise Exception(f"Row {row} out of bounds")
        if col < 0 or col >= self.cols:
            return False
        
        return self._grid[row][col] is not None
    
    # Testing only: Grid should not be aware of directions
    def pedestrian_passed(self, grid_direction: Direction):
        if grid_direction == "East":
            self._passed_to_east += 1
        elif grid_direction == "West":
            self._passed_to_west += 1

    def show(self):
        print(f"{'': ^2}", end="")
        for i in range(self.cols):
            # if even, print with color red, else print with color blue
            if i % 2 == 0:
                print("\033[91m", end="")
            else:
                print("\033[94m", end="")
            print(f"{i: >2}", end="")
            print("\033[0m", end="")
        print()
        for i in range(END_ROW):

            # if i < CROSSWALK_START_ROW:
            #    continue
            if i % 2 == 0:
                print("\033[91m", end="")
            else:
                print("\033[94m", end="")
            print(f"{i: ^2}", end="")
            print("\033[0m", end="")
            for j in range(self.cols):
                if self.is_fill(i, j):
                    value = self._grid[i][j]
                    if value.__class__.__name__ == "Pedestrian":
                        if value.facing == "East":
                            print(f"{self._grid[i][j]._repr}", end="")
                        else:
                            print(f"{self._grid[i][j]._repr}", end="")
                    else:
                        print(f"{self._grid[i][j]._repr}", end="")
                else:
                    if CROSSWALK_START_ROW <= i < CROSSWALK_END_ROW and j % 4 <= 1:
                        print(f"{'⬜'}", end="")
                    else:
                        print(f"{'⬛'}", end="")

            print()
        

    def fill(self, row: int, col: int, v: T):
        if self.is_fill(row, col):
            raise CellAlreadyFill(row, col, self._grid[row][col])
            
        self._grid[row][col] = v

    def clear(self, row: int, col: int):
        if not self.is_fill(row, col):
            raise Exception(f"Attempted to clear an empty cell ({row}, {col})")
        
        self._grid[row][col] = None

    def get_value(self, row: int, col: int) -> T:
        if not self.is_fill(row, col):
            raise Exception(f"Element not found at row {row}, col {col}")
        return self._grid[row][col]

    @property
    def rows(self):
        return len(self._grid)

    @property
    def cols(self):
        return len(self._grid[0])

    def calc_dist_to_next(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[int]:
        if f is None:
            f = lambda x: True

        for i in range(col+1, self.cols):
            if self.is_fill(row, i) and f(self.get_value(row, i)):
                return i - col - 1
        return None
    
    def calc_dist_to_prev(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[int]:
        if f is None:
            f = lambda x: True

        for i in range(col-1, -1, -1):
            if self.is_fill(row, i) and f(self.get_value(row, i)):
                return col - i - 1
        return None
    
    def calc_dist_to_vertically_next(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[int]:
        if f is None:
            f = lambda x: True

        for i in range(row+1, self.rows):
            if self.is_fill(i, col) and f(self.get_value(i, col)):
                return i - row - 1
        return None
    
    def calc_dist_to_vertically_prev(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[int]:
        if f is None:
            f = lambda x: True

        for i in range(row-1, -1, -1):
            if self.is_fill(i, col) and f(self.get_value(i, col)):
                return row - i - 1
        return None
    
    def get_prev(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[T]:
        dist = self.calc_dist_to_prev(row, col, f)
        if dist is None:
            return None
        return self.get_value(row, col - dist - 1)
    
    def get_vertically_prev(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[T]:
        dist = self.calc_dist_to_vertically_prev(row, col, f)
        if dist is None:
            return None
        return self.get_value(row - dist - 1, col)
    
    def get_next(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[T]:
        dist = self.calc_dist_to_next(row, col, f)
        if dist is None:
            return None
        return self.get_value(row, col + dist + 1)
    
    def get_vertically_next(self, row: int, col: int, f: Callable[[T], bool] = None) -> Optional[T]:
        dist = self.calc_dist_to_vertically_next(row, col, f)
        if dist is None:
            return None
        return self.get_value(row + dist + 1, col)
    
    def apply(self, f: Callable[[T, Tuple[int, int]], None]):
        remaining_cells = [(i, j) for i in range(self.rows) for j in range(self.cols)]

        while len(remaining_cells) > 0:
            cell = gen.choice(remaining_cells)
            remaining_cells.remove(cell)
            i, j = cell
            if self.is_fill(i, j):
                f(self.get_value(i, j), (i, j))