from typing import List

from rectangle import Rectangle, Point
from config import Config
from grid.grid import Grid

class Plotter:
    def __init__(self, grid: Grid, config: Config):
        self._config = config
        self._grid = grid
        self._bounds = Rectangle(self._config.crosswalk_prot.rows + self._config.vehicle_prot.rows,
                                 self._config.total_cols)
        self._bounds.move_down(self._config.vehicle_prot.rows)
        print(f"Bounds: {self._bounds}")
        crosswalk_start_row = self._config.vehicle_prot.rows
        crosswalk_start_col = self._config.waiting_area_prot.cols

        self._crosswalk_zone = self._config.crosswalk_prot.duplicate()
        self._crosswalk_zone.move_right(crosswalk_start_col)
        self._crosswalk_zone.move_down(crosswalk_start_row)

        self._waiting_area_zones: List[Rectangle] = []
        waiting_area_west_zone = self._config.waiting_area_prot.duplicate()
        waiting_area_west_zone.move_down(crosswalk_start_row)
        self._waiting_area_zones.append(waiting_area_west_zone)

        waiting_area_east_zone = self._config.waiting_area_prot.duplicate()
        waiting_area_east_zone.move_right(self._config.waiting_area_prot.cols + self._crosswalk_zone.cols)
        waiting_area_east_zone.move_down(crosswalk_start_row)
        self._waiting_area_zones.append(waiting_area_east_zone)

    def plot(self):
        self._grid.plot(self._plot_object, self._bounds)

    def _plot_object(self, point: Point, obj) -> str:
        _, col = point
        if obj is None:
             for waiting_area_zone in self._waiting_area_zones:
                if waiting_area_zone.is_inside(point):
                    return f"{'🔳'}"
                
             if self._crosswalk_zone.is_inside(point) and col % 4 <= 1:
                return f"{'⬜'}"
             else:
                return f"{'⬛'}"
        else:
            return obj._repr
