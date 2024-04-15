import pytest

from ..grid import Grid

def test_grid_creation():
    grid = Grid[int](5, 3)
    assert grid.width == 5
    assert grid.length == 3

def test_grid_fill():
    grid = Grid[int](5, 3)
    grid.fill(2, 1, 128)
    
    assert grid.is_fill(2, 1)

def test_grid_fill_two_times_same_cell_should_raise_exception():
    grid = Grid[int](5, 3)
    grid.fill(2, 1, 128)
    
    with pytest.raises(Exception) as e:
        grid.fill(2, 1, 128)

def test_grid_get_value():
    grid = Grid[int](5, 3)
    grid.fill(2, 1, 128)
    
    assert grid.get_value(2, 1) == 128

def test_grid_get_empty_value_should_raise_exception():
    grid = Grid[int](5, 3)
    
    with pytest.raises(Exception) as e:
        grid.get_value(2, 1)

def test_get_dist_to_next():
    grid = Grid[str](1, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . . X . Y . . . .
    """

    grid.fill(0, 3, "X")
    grid.fill(0, 5, "Y")

    assert grid.calc_dist_to_next(0, 3) == 1

def test_get_dist_to_prev():
    grid = Grid[str](1, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . Y . . X . . . .
    """

    grid.fill(0, 5, "X")
    grid.fill(0, 2, "Y")

    assert grid.calc_dist_to_prev(0, 5) == 2

def test_get_dist_to_next_returns_none_if_no_next_value():
    grid = Grid[str](1, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . . X . . . . . .
    """

    grid.fill(0, 3, "X")

    assert grid.calc_dist_to_next(0, 3) is None

def test_get_dist_to_prev_returns_none_if_no_prev_value():
    grid = Grid[str](1, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . . . . X . . . .
    """

    grid.fill(0, 5, "X")

    assert grid.calc_dist_to_prev(0, 5) is None

def test_get_next():
    grid = Grid[str](1, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . . X . Y . . . .
    """

    grid.fill(0, 3, "X")
    grid.fill(0, 5, "Y")

    assert grid.get_next(0, 3) == "Y"

def test_get_prev():
    grid = Grid[str](1, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . Y . . X . . . .
    """

    grid.fill(0, 5, "X")
    grid.fill(0, 2, "Y")

    assert grid.get_prev(0, 5) == "Y"