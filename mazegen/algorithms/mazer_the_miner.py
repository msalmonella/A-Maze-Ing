import sys
from random import Random
from collections.abc import Generator
from . import Algorithm
from ..models import Coordinate, Direction
from ..errors import LockedWallError
from ..cell import Grid
from ..models import Mandatory


class MazerTheMiner(Algorithm):

    def __call__(
        self, grid: Grid, config: Mandatory, rng: Random
    ) -> Generator[None]:
        self._apply_recursion_limit(config.width, config.height)
        return self.mazer_the_miner(grid, rng, Coordinate(0, 0), set())

    def mazer_the_miner(
        self,
        grid: Grid,
        rng: Random,
        head: Coordinate,
        processed: set[Coordinate],
    ) -> Generator[None]:
        """Recursive function to create maze by digging into walls"""

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
        cell_count = width * height
        wall_count = 4
        needed = cell_count * wall_count
        if needed > sys.getrecursionlimit():
            sys.setrecursionlimit(needed)
