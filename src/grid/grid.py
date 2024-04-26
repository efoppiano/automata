from typing import TypeVar, Generic, Optional, Callable, Tuple, List

from generator.tp_generator import choice
from rectangle import Point, Rectangle

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

    def is_fill(self, row: int, col: int) -> bool:
        if row < 0 or row >= self.rows:
            return False
        if col < 0 or col >= self.cols:
            return False
        
        return self._grid[row][col] is not None

    def _plot_col_numbers(self, bounds: Rectangle):
        print("  ", end="")
        for col in range(bounds.start_col, bounds.end_col+1):
            if col % 2 == 0:
                print("\033[91m", end="")
            else:
                print("\033[94m", end="")
            print(f"{col: >2}", end="")
            print("\033[0m", end="")
        print()

    def _plot_row_number(self, row: int):
        if row % 2 == 0:
            print("\033[91m", end="")
        else:
            print("\033[94m", end="")
        print(f"{row: ^2}", end="")
        print("\033[0m", end="")

    def plot(self, f: Callable[[Point, Optional[T]], Optional[str]], bounds: Rectangle = None):
        if bounds is None:
            bounds = Rectangle(self.rows, self.cols)

        self._plot_col_numbers(bounds)

        for row in range(bounds.start_row, bounds.end_row+1):
            self._plot_row_number(row)
            
            for col in range(bounds.start_col, bounds.end_col+1):
                if not bounds.is_inside((row, col)):
                    continue
                if self.is_fill(row, col):
                    s = f((row, col), self.get_value(row, col))
                else:
                    s = f((row, col), None)
                print(s, end="")
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

    def calc_dist_to_next(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[int]:
        if f is None:
            f = lambda x: True
        max_checks = max_checks or self.cols - col
        
        for i in range(col+1, min(self.cols, col+max_checks+1)):
            if self.is_fill(row, i) and f(self.get_value(row, i)):
                return i - col - 1
        return None
    
    def calc_dist_to_prev(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[int]:
        if f is None:
            f = lambda x: True
        max_checks = max_checks or col

        for i in range(col-1, max(-1, col-max_checks-1), -1):
            if self.is_fill(row, i) and f(self.get_value(row, i)):
                return col - i - 1
        return None
    
    def calc_dist_to_vertically_next(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[int]:
        if f is None:
            f = lambda x: True
        max_checks = max_checks or self.rows - row

        for i in range(row+1, min(self.rows, row+max_checks+1)):
            if self.is_fill(i, col) and f(self.get_value(i, col)):
                return i - row - 1
        return None
    
    def calc_dist_to_vertically_prev(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[int]:
        if f is None:
            f = lambda x: True
        max_checks = max_checks or row

        for i in range(row-1, max(-1, row-max_checks-1), -1):
            if self.is_fill(i, col) and f(self.get_value(i, col)):
                return row - i - 1
            
        return None
    
    def get_prev(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[T]:
        max_checks = max_checks or col

        dist = self.calc_dist_to_prev(row, col, f, max_checks)
        if dist is None:
            return None
        return self.get_value(row, col - dist - 1)
    
    def get_vertically_prev(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[T]:
        max_checks = max_checks or row

        dist = self.calc_dist_to_vertically_prev(row, col, f, max_checks)
        if dist is None:
            return None
        return self.get_value(row - dist - 1, col)
    
    def get_next(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[T]:
        max_checks = max_checks or self.cols - col

        dist = self.calc_dist_to_next(row, col, f, max_checks)
        if dist is None:
            return None
        return self.get_value(row, col + dist + 1)
    
    def get_vertically_next(self, row: int, col: int, f: Callable[[T], bool] = None, max_checks: int = None) -> Optional[T]:
        max_checks = max_checks or self.rows

        dist = self.calc_dist_to_vertically_next(row, col, f, max_checks)
        if dist is None:
            return None
        return self.get_value(row + dist + 1, col)
    
    def _get_cells_with_value(self) -> List[Tuple[Tuple[int, int], T]]:
        values = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_fill(i, j):
                    values.append(((i, j), self.get_value(i, j)))
        return values
    
    def apply(self, f: Callable[[T, Tuple[int, int]], None]):
        values = self._get_cells_with_value()

        while len(values) > 0:
            cell = choice(values)
            values.remove(cell)
            pos, value = cell
            f(value, pos)