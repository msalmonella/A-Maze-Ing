from random import Random
from collections.abc import Generator
from . import Algorithm
from ..cell import Wall, Grid
from ..models import Coordinate
from ..models import Mandatory


class Prim(Algorithm):
    """Generates a maze using randomized Prim's algorithm."""

    def __call__(
        self, grid: Grid, config: Mandatory, rng: Random
    ) -> Generator[None]:
        return self.prim(grid, config, rng)

    def prim(
        self,
        grid: Grid,
        config: Mandatory,
        rng: Random,
    ) -> Generator[None]:
        """Function to create maze by Prim's minimal spanning tree algorithm"""

        frontiers: list[tuple[Wall, Coordinate]] = []
        visited: set[Coordinate] = {config.entry}

        def add_frontiers(coord: Coordinate) -> None:
            x, y = coord
            cell = grid[y][x]

            for direction, wall in cell.walls.items():
                if not wall.locked:
                    next_cell = cell.neighbor(direction)
                    if next_cell not in visited:
                        frontiers.append((wall, next_cell))

        add_frontiers(config.entry)

        while frontiers:
            frontier, coord = frontiers.pop(rng.randrange(len(frontiers)))

            if coord in visited:
                continue
            visited.add(coord)
            frontier.closed = False
            add_frontiers(coord)
            yield
