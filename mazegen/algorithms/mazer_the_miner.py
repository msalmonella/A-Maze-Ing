"""Maze generation algorithm using recursive wall digging."""

import sys
from random import Random
from collections.abc import Generator
from . import Algorithm
from ..models import Coordinate, Direction
from ..errors import LockedWallError
from ..cell import Grid
from ..models import Mandatory


class MazerTheMiner(Algorithm):
    """Generate a maze by recursively digging through walls."""

    def __call__(
        self, grid: Grid, config: Mandatory, rng: Random
    ) -> Generator[None]:
        """Generate a maze using the Mazer the Miner algorithm.

        Args:
            grid (Grid): The grid in which the maze will be generated.
            config (Mandatory):
                Maze configuration containing the grid dimensions.
            rng (random.Random):
                Random number generator used to randomize directions.

        Returns:
            Generator: A generator that yields after each wall is opened.
        """

        self._apply_recursion_limit(config.width, config.height)
        return self.mazer_the_miner(grid, rng, Coordinate(0, 0), set())

    def mazer_the_miner(
        self,
        grid: Grid,
        rng: Random,
        head: Coordinate,
        processed: set[Coordinate],
    ) -> Generator[None]:
        """Recursively generate a maze by digging through walls.

        Args:
            grid (Grid): The grid in which the maze is being generated.
            rng (Random): Random number generator used to randomize directions.
            head (Coordinate): Coordinate of the current cell being processed.
            processed (set[Coordinate]):
                Set of coordinates that have already been visited.

        Yields:
            Generator: None after successfully opening a wall.
        """

        x, y = head
        cell = grid[y][x]
        processed.add(head)

        directions = list(Direction)
        rng.shuffle(directions)

        for direction in directions:
            next_index = cell.neighbor(direction)

            if next_index not in processed:
                try:
                    wall = cell.walls[direction]
                    wall.closed = False
                    yield
                except LockedWallError:
                    continue

                yield from self.mazer_the_miner(
                    grid, rng, next_index, processed
                )

    @staticmethod
    def _apply_recursion_limit(width: int, height: int) -> None:
        """Increase the recursion limit when the grid requires it.

        Args:
            width (int): Width of the maze grid in cells.
            height (int): Height of the maze grid in cells.
        """

        cell_count = width * height
        wall_count = 4
        needed = cell_count * wall_count
        if needed > sys.getrecursionlimit():
            sys.setrecursionlimit(needed)
