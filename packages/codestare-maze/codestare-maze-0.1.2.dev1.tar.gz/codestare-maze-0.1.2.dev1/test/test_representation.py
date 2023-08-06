"""
Test some simple functionality
"""
from contextlib import suppress
from typing import List

import pytest

from codestare.mazes.representation import Grid, Direction as Di


def directions(data) -> List[List[Di]]:
    """convert series of numbers to path directions in a grid"""
    cells = []

    for y, row in enumerate(data):
        c = [Di.NONE] * len(row)
        for x, cell in enumerate(row):
            for direct in [Di.E, Di.N, Di.S, Di.W]:
                with suppress(IndexError):
                    if data[y + direct.dy][x + direct.dx] == data[y][x]:
                        c[x] |= direct
        cells.append(c)

    return cells


@pytest.fixture
def grid(request) -> Grid:
    """returns a parameterizable grid"""
    param = getattr(request, 'param', {})
    height, width = param.get('dimensions', (4, 4))
    grid = Grid(height=height, width=width)
    data = param.get('data', None)

    if data:
        grid.data = data

    yield grid


@pytest.mark.parametrize(
    'grid, items, expected', [
        [
            {
                'data': directions([
                    [1, 0, 1, 0],
                    [1, 1, 1, 1],
                    [0, 1, 0, 0],
                    [0, 1, 1, 1],
                ])
            },
            [(0, 0), (-1, 0)],
            [Di.S, None]
        ],
    ],
    indirect=['grid']
)
def test_display(grid, items, expected):
    for (x, y), expect in zip(items, expected):
        assert grid[x, y] == expect

    grid.display_maze()


@pytest.mark.parametrize(
    'grid, value', [
        [{'dimensions': (60, 60), 'data': [[Di.N] * 60 for _ in range(60)]}, Di.N],
        [{'dimensions': (60, 60), 'data': [[Di.ALL] * 60 for _ in range(60)]}, Di.ALL],
    ],
    indirect=['grid']
)
def test_set_all(grid: Grid, value):
    for y in range(grid.height):
        for x in range(grid.width):
            assert grid[x, y] == value

    grid.display_maze()
