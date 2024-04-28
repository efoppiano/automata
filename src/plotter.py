import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
from matplotlib.animation import ArtistAnimation, FuncAnimation

from typing import List

from rectangle import Rectangle, Point
from config import Config
from grid.grid import Grid
from road_entity import RoadEntity
from images import squares, place_image

class Plotter:
    def __init__(self, grid: Grid, config: Config, animate: bool = True):
        self._config = config
        self._grid = grid
        self._bounds = Rectangle(self._config.crosswalk_prot.rows + self._config.vehicle_prot.rows,
                                 self._config.total_cols)
        self._bounds.move_down(self._config.vehicle_prot.rows)
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

        self._animate = animate
        if animate:
            self._imgs: List[List[AxesImage]] = []
            fig, ax = plt.subplots(figsize=(16, 9))
            self._fig = fig
            self._ax: plt.Axes = ax
            self.configure_plot()
            self._background = self.get_background_imgs()

    def get_background_imgs(self) -> List[AxesImage]:
        imgs = []
        for row in range(self._bounds.start_row, self._bounds.end_row + 1):
            for col in range(self._bounds.start_col, self._bounds.end_col + 1):
                background_emoji_str = self.get_backgound_emoji_at((row, col))
                img = place_image(self._ax, squares[background_emoji_str], col, row)
                imgs.append(img)
        return imgs

    def configure_plot(self):
        self._ax.set_xlim(self._bounds.start_col, self._bounds.end_col+1)
        self._ax.set_ylim(self._bounds.end_row-2, self._bounds.start_row)
        self._ax.set_xticks(range(self._bounds.start_col, self._bounds.end_col + 1))
        self._ax.set_yticks(range(self._bounds.start_row, self._bounds.end_row + 2))
        self._ax.grid(True, color="black")
        self._fig.tight_layout()

    def add_frame(self):
        imgs_frames = []

        self._grid.apply_ordered(self._bounds, lambda obj, _: imgs_frames.extend(obj.plot_in_ax(self._ax)))
        self._imgs.append(imgs_frames)
    
    def save_mp4(self, filename: str):
        anim = ArtistAnimation(self._fig, self._imgs, interval=200, blit=True)
        anim.save(filename, writer='ffmpeg')

    def get_backgound_emoji_at(self, point: Point) -> str:
        _, col = point
        for waiting_area_zone in self._waiting_area_zones:
            if waiting_area_zone.is_inside(point):
                return f"{'🔳'}"    
        if self._crosswalk_zone.is_inside(point) and col % 4 <= 1:
            return f"{'⬜'}"
        else:
            return f"{'⬛'}"

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
