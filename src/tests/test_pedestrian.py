from typing import List, Dict, Tuple

from ..grid import Grid
from ..relative_grid import RelativeGrid
from ..movements import Forward, TurnLeft, TurnRight
from ..pedestrian import Pedestrian

def build_test_grid(values: List[str], velocities: Dict[str, int] = {}) \
    -> Tuple[Grid[Pedestrian], Dict[str, Pedestrian], Dict[str, Tuple[int, int]]]:

    rows = len(values)
    cols = len(values[0].split())

    grid = Grid[Pedestrian](rows, cols)
    pedestrians = {}
    positions = {}

    for i, row in enumerate(values):
        for j, value in enumerate(row.split()):
            if value != "[]":
                if value[-1] == ">":
                    value = value[:-1]
                    direction = "East"
                elif value[0] == "<":
                    value = value[1:]
                    direction = "West"
                else:
                    direction = "East"
                velocity = velocities.get(value, 1)
                pedestrian = Pedestrian(direction, velocity)
                grid.fill(i, j, pedestrian)
                pedestrians[value] = pedestrian
                positions[value] = (i, j)

    return grid, pedestrians, positions

def test_pedestrian_init():
    pedestrian = Pedestrian("East", 6)

    assert pedestrian._vel == 6
    assert pedestrian._facing == "East"

def test_pedestrian_with_blocked_path():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] X> Y> [] [] [] [] []",
    ])

    rel_grid = RelativeGrid[Pedestrian](positions["X"], "East", grid)
    
    assert not pedestrians["X"].can_move_forward(rel_grid)

def test_pedestrian_without_blocked_path():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] X> [] Y> [] [] [] []",
    ])

    rel_grid = RelativeGrid[Pedestrian](positions["X"], "East", grid)
    
    assert pedestrians["X"].can_move_forward(rel_grid)

def test_pedestrian_that_can_move_left():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] [] [] [] <Y [] []",
        "[] [] [] X> [] [] [] [] [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_y = RelativeGrid[Pedestrian](positions["Y"], pedestrians["Y"].facing, grid)
    
    assert pedestrians["X"].can_move_left(rel_grid_x)
    assert pedestrians["Y"].can_move_left(rel_grid_y)

def test_pedestrian_that_cannot_move_left_because_it_is_the_end_of_crosswalk():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] [] [] Y> [] [] []",
        "[] [] [] <X [] [] [] [] [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_y = RelativeGrid[Pedestrian](positions["Y"], pedestrians["Y"].facing, grid)

    assert not pedestrians["X"].can_move_left(rel_grid_x)
    assert not pedestrians["Y"].can_move_left(rel_grid_y)

def test_pedestrian_that_cannot_move_left_because_the_cell_is_occupied():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] Y> [] [] [] <W [] []",
        "[] [] [] X> [] [] [] <Z [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_w = RelativeGrid[Pedestrian](positions["W"], pedestrians["W"].facing, grid)

    assert not pedestrians["X"].can_move_left(rel_grid_x)
    assert not pedestrians["W"].can_move_left(rel_grid_w)

def test_pedestrian_that_cannot_move_left_because_there_is_a_pedestrian_ahead():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] [] Y> [] [] [] <Z",
        "[] [] [] X> [] [] [] <W [] []",
    ], velocities={"X": 1, "Z": 1})

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_z = RelativeGrid[Pedestrian](positions["Z"], pedestrians["Z"].facing, grid)

    assert not pedestrians["X"].can_move_left(rel_grid_x)
    assert not pedestrians["Z"].can_move_left(rel_grid_z)

def test_pedestrian_can_move_left_if_pedestrian_ahead_is_far_enough():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] Y> [] [] [] [] [] <Z",
        "X> [] [] [] [] <W [] [] [] []",
    ], velocities={"X": 1, "Z": 1})

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_z = RelativeGrid[Pedestrian](positions["Z"], pedestrians["Z"].facing, grid)

    assert pedestrians["X"].can_move_left(rel_grid_x)
    assert pedestrians["Z"].can_move_left(rel_grid_z)

def test_pedestrian_that_can_move_right():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] [] [] [] Y> [] []",
        "[] [] [] <X [] [] [] [] [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_y = RelativeGrid[Pedestrian](positions["Y"], pedestrians["Y"].facing, grid)
    
    assert pedestrians["X"].can_move_right(rel_grid_x)
    assert pedestrians["Y"].can_move_right(rel_grid_y)

def test_pedestrian_that_cannot_move_right_because_it_is_the_end_of_crosswalk():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] [] [] [] <Y [] []",
        "[] [] [] X> [] [] [] [] [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_y = RelativeGrid[Pedestrian](positions["Y"], pedestrians["Y"].facing, grid)

    assert not pedestrians["X"].can_move_right(rel_grid_x)
    assert not pedestrians["Y"].can_move_right(rel_grid_y)

def test_pedestrian_that_cannot_move_right_because_the_cell_is_occupied():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] Y> [] [] [] X> [] []",
        "[] [] [] <W [] [] [] Z> [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)
    rel_grid_w = RelativeGrid[Pedestrian](positions["W"], pedestrians["W"].facing, grid)

    assert not pedestrians["X"].can_move_right(rel_grid_x)
    assert not pedestrians["W"].can_move_right(rel_grid_w)

def test_pedestrian_that_cannot_move_right_because_there_is_a_pedestrian_ahead():
    grid, pedestrians, positions = build_test_grid([
        "[] <X [] [] [] [] [] Z> [] [] []",
        "[] [] [] <Y [] [] [] [] [] W> []",
    ], velocities={"Y": 1, "Z": 1})

    rel_grid_y = RelativeGrid[Pedestrian](positions["Y"], pedestrians["Y"].facing, grid)
    rel_grid_z = RelativeGrid[Pedestrian](positions["Z"], pedestrians["Z"].facing, grid)

    assert not pedestrians["Y"].can_move_right(rel_grid_y)
    assert not pedestrians["Z"].can_move_right(rel_grid_z)

def test_pedestrian_can_move_right_if_pedestrian_ahead_is_far_enough():
    grid, pedestrians, positions = build_test_grid([
        "[] <X [] [] [] [] Z> [] [] [] []",
        "[] [] [] [] <Y [] [] [] [] W> []",
    ], velocities={"Y": 1, "Z": 1})

    rel_grid_y = RelativeGrid[Pedestrian](positions["Y"], pedestrians["Y"].facing, grid)
    rel_grid_z = RelativeGrid[Pedestrian](positions["Z"], pedestrians["Z"].facing, grid)

    assert pedestrians["Y"].can_move_right(rel_grid_y)
    assert pedestrians["Z"].can_move_right(rel_grid_z)

def test_pedestrian_choose_forward_if_no_obstacles():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] Y> [] [] [] [] []",
        "[] [] [] X> [] [] [] [] [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)

    pedestrians["X"].think(rel_grid_x)
    assert pedestrians["X"]._desired_movement == Forward(1)

def test_pedestrian_choose_left_if_there_are_obstacles():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] [] [] [] [] [] []",
        "[] [] [] X> Y> [] [] [] [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)

    pedestrians["X"].think(rel_grid_x)
    assert pedestrians["X"]._desired_movement == TurnLeft(1)

def test_pedestrian_choose_right_if_there_are_obstacles():
    grid, pedestrians, positions = build_test_grid([
        "[] [] [] [] [] [] [] [] [] []",
        "[] [] [] [] <Y <X [] [] [] []",
    ])

    rel_grid_x = RelativeGrid[Pedestrian](positions["X"], pedestrians["X"].facing, grid)

    pedestrians["X"].think(rel_grid_x)

    assert pedestrians["X"]._desired_movement == TurnRight(1)