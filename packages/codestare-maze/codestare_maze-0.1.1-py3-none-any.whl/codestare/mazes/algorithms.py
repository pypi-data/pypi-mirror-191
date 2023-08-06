"""
Collection of maze generating algorithms
"""
import functools
import logging
import random as rand
from typing import Sequence

from .representation import Grid, Direction

log = logging.getLogger(__name__)


class GrowingTree:
    """
    The growing tree algorithm can be adjusted to be recursive backtracking or Prim's algorithm
    (and more) depending on the choice of next element.
    """
    random = rand.choice

    @staticmethod
    def last(live: Sequence):
        """Chooses last added live cell"""
        return live[-1]

    @staticmethod
    def mixed(live: Sequence, threshold=0.2):
        """Switches between choosing last added cell and random cell depending on threshold"""
        sub_choice = GrowingTree.last if rand.random() > threshold else GrowingTree.random
        return sub_choice(live)

    def __call__(self, args):
        h = getattr(args, 'h', 40)
        w = getattr(args, 'w', 40)
        threshold = getattr(args, 't', 0)
        choice = globals().get(args.choice, functools.partial(self.mixed, threshold=threshold))
        grid = Grid(height=h, width=w)
        del threshold

        cell_positions = set((w_, h_) for h_ in range(h) for w_ in range(w))
        del h, w

        directions = [Direction.E, Direction.W, Direction.S, Direction.N]
        live = [rand.choice(list(cell_positions))]
        cell_positions.remove(live[-1])

        while live:
            x, y = choice(live)
            rand.shuffle(directions)
            neighbor, direction = None, None

            for direction in directions:
                candidate = (x + direction.dx, y + direction.dy)
                if candidate in cell_positions:
                    neighbor = candidate
                    cell_positions.remove(neighbor)
                    break

            if neighbor:
                live.append(neighbor)
                grid.carve(start=(x, y), direction=direction)
            else:
                live.remove((x, y))

            log.debug(f"{len(live)} cells live, {len(cell_positions)} not visited")

        grid.display_maze()


growing_tree = GrowingTree()
"""growing tree implementation"""
