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

def test_grid_is_forward_fill():
    grid = Grid[str](1, 2)
    grid.fill(0, 1, "X")
    
    assert grid.is_forward_fill(0, 0, "East")
    assert not grid.is_forward_fill(0, 0, "West")

def test_grid_is_left_fill():
    grid = Grid[str](2, 1)
    grid.fill(0, 0, "X")
    
    assert grid.is_left_fill(1, 0, "East")

def test_grid_is_right_fill():
    grid = Grid[str](2, 1)
    grid.fill(0, 0, "X")
    
    assert grid.is_right_fill(1, 0, "West")

def test_grid_is_left_fill_should_raise_exception_when_out_of_bounds():
    grid = Grid[str](2, 1)
    
    with pytest.raises(Exception) as e:
        grid.is_left_fill(0, 0, "East")

def test_grid_is_right_fill_should_raise_exception_when_out_of_bounds():
    grid = Grid[str](2, 1)
    
    with pytest.raises(Exception) as e:
        grid.is_right_fill(1, 0, "East")

def test_grid_dist_to_next_value():
    grid = Grid[str](10, 10)

    grid.fill(0, 5, "X")
    grid.fill(0, 8, "X")

    assert grid.dist_to_next_value(0, 2, "East") == 2
    assert grid.dist_to_next_value(0, 2, "West") is None
    assert grid.dist_to_next_value(1, 9, "West") is None

def test_grid_get_prev_value_left():
    grid = Grid[str](10, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . . Y . . . . . .
    . . . . . X . . . .
    """
    grid.fill(1, 5, "X")
    grid.fill(0, 3, "Y")

    assert grid.get_prev_value_left(1, 5, "East") == "Y"
    assert grid.get_prev_value_left(1, 3, "East") is None
    assert grid.get_prev_value_left(1, 5, "West") is None
    assert grid.get_prev_value_left(0, 3, "West") == "X"

def test_grid_get_prev_value_right():
    grid = Grid[str](10, 10)

    """
    The grid looks like this:
    0 1 2 3 4 5 6 7 8 9
    . . . . . Y . . . .
    . . . X . . . . . .
    """

    grid.fill(0, 5, "Y")
    grid.fill(1, 3, "X")

    assert grid.get_prev_value_right(0, 5, "East") == "X"
    assert grid.get_prev_value_right(1, 3, "West") == "Y"
    assert grid.get_prev_value_right(0, 2, "East") is None
    assert grid.get_prev_value_right(1, 6, "West") is None

