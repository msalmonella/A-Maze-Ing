"""Maze generation using randomized Prim's minimum spanning tree algorithm."""

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
        """Generate a maze using randomized Prim's algorithm.

        Args:
            grid (Grid): The grid in which the maze will be generated.
            config (Mandatory):
                Maze configuration containing the entry coordinate.
            rng (random.Random):
                Random number generator used to select frontiers.

        Returns:
            A generator that yields after each wall is opened.
        """
        return self.prim(grid, config, rng)

    def prim(
        self,
        grid: Grid,
        config: Mandatory,
        rng: Random,
    ) -> Generator[None]:
        """Method to create maze by Prim's minimal spanning tree algorithm.

        Args:
            grid (Grid): The grid in which the maze will be generated.
            config (Mandatory):
                Maze configuration containing the entry coordinate.
            rng (random.Random):
                Random number generator used to select frontiers.

        Yields:
            None after successfully opening a wall between a visited cell
            and a frontier cell.
        """

        frontiers: list[tuple[Wall, Coordinate]] = []
        visited: set[Coordinate] = set()

        def add_frontiers(coord: Coordinate) -> None:
            """Add unvisited neighboring cells to the frontier list.

            Args:
                coord (Coordinate):
                    Coordinate of the cell whose neighbors are added to the
                    frontier list.
            """

            x, y = coord
            cell = grid[y][x]

            for direction, wall in cell.walls.items():
                if not wall.locked:
                    next_cell = cell.neighbor(direction)
                    if next_cell not in visited:
                        frontiers.append((wall, next_cell))

        while not frontiers:
            start_point = Coordinate(
                rng.randrange(0, config.width) if config.width else 0,
                rng.randrange(0, config.height) if config.height else 0,
            )
            add_frontiers(start_point)

        while frontiers:
            frontier, coord = frontiers.pop(rng.randrange(len(frontiers)))

            if coord in visited:
                continue
            visited.add(coord)
            frontier.closed = False
            add_frontiers(coord)
            yield
