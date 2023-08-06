"""
data representation for mazes
"""
from __future__ import annotations

from contextlib import suppress
from enum import auto, IntFlag
from typing import Literal, Tuple


def neighbor(pos: Tuple[int, int], direction: Direction):
    """calculate indices of neighbor in direction"""
    x, y = pos
    return x + direction.dx, y + direction.dy


class Grid:
    """represents a grid shape labyrinth"""
    def __init__(self, height: int, width: int):
        self.data = [[Direction.NONE] * width for _ in range(height)]

    @property
    def height(self):
        """height of the grid"""
        return len(self.data) if self.data else None

    @property
    def width(self):
        """width of the grid"""
        return len(self.data[0]) if self.data else None

    def __getitem__(self, item):
        """instead of index errors for elements outside the grid return None"""
        x, y = item
        if x >= self.width or x < 0:
            return None
        if y >= self.height or y < 0:
            return None
        else:
            return self.data[y][x]

    def __setitem__(self, key, value):
        """instead of index errors when attempting to set elements outside the grid, don't do anything"""
        x, y = key
        if x >= self.width or x < 0:
            return
        if y >= self.height or y < 0:
            return
        else:
            self.data[y][x] = value

    def carve(self, start: Tuple[int, int], direction: Direction):
        """'carve' a connection from start in direction"""
        x, y = start
        with suppress(TypeError):
            self[start] |= direction
            self[x + direction.dx, y + direction.dy] |= direction.opposite

    def display_maze(self):
        """displays the maze"""
        print()

        def wall(pos, direction):
            """calculates if there is a wall in the specified direction"""
            n = self[neighbor(pos, direction)]
            real_cell = self[pos] is not None
            real_neighbor = n is not None
            return (direction.opposite not in n) if (real_cell and real_neighbor) else (real_cell ^ real_neighbor)

        # iterate over junctions (represented as directions)
        for y in range(self.height + 1):
            out = []
            for x in range(self.width + 1):
                pos = (x, y)
                junction = Direction.NONE
                # wall in southern direction
                if wall(pos, Direction.W):
                    junction |= Direction.S
                # wall in west direction
                if wall(neighbor(pos, Direction.W), Direction.N):
                    junction |= Direction.W
                # wall in north direction
                if wall(neighbor(pos, Direction.N), Direction.W):
                    junction |= Direction.N
                # wall in east direction
                if wall(pos, Direction.N):
                    junction |= Direction.E

                out += [junction.char]

            print(''.join(out))


class Direction(IntFlag):
    """direction in a maze, can represent paths or walls or anything else"""
    NONE = 0
    N = auto()
    E = auto()
    S = auto()
    W = auto()
    ALL = N | E | S | W

    def __contains__(self, item):
        """check if flag is set"""
        return self & item == item

    @property
    def dx(self) -> Literal[0, 1, -1] | None:
        """dx is 1 in east direction and -1 in west direction"""
        if Direction.E | Direction.W in self:
            return None
        if Direction.E in self:
            return 1
        if Direction.W in self:
            return -1

        return 0

    @property
    def dy(self) -> Literal[0, 1, -1] | None:
        """dy is 1 in north direction and -1 in south direction"""
        if Direction.N | Direction.S in self:
            return None
        if Direction.N in self:
            return -1
        if Direction.S in self:
            return 1

        return 0

    @property
    def opposite(self):
        """the 4 major directions have opposites"""
        if self == Direction.E:
            return Direction.W
        if self == Direction.W:
            return Direction.E
        if self == Direction.S:
            return Direction.N
        if self == Direction.N:
            return Direction.S

    @property
    def char(self):
        """if you represent walls as directions, this property returns the appropriate unicode box drawing char"""
        if self == Direction.E:
            return '╶'
        if self == Direction.W:
            return '╴'
        if self == Direction.S:
            return '╷'
        if self == Direction.N:
            return '╵'
        if self == (Direction.N | Direction.E):
            return '└'
        if self == (Direction.S | Direction.E):
            return '┌'
        if self == (Direction.N | Direction.W):
            return '┘'
        if self == (Direction.S | Direction.W):
            return '┐'
        if self == (Direction.E | Direction.W):
            return '─'
        if self == (Direction.N | Direction.S):
            return '│'
        if self == (Direction.ALL & ~Direction.S):
            return '┴'
        if self == (Direction.ALL & ~Direction.N):
            return '┬'
        if self == (Direction.ALL & ~Direction.E):
            return '┤'
        if self == (Direction.ALL & ~Direction.W):
            return '├'
        if self == Direction.ALL:
            return '┼'
        if self == ~Direction.ALL:
            return ' '

    def __str__(self):
        return repr(self)
