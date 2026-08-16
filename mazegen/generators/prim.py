from random import Random
from typing import assert_never
import mazegen
from . import Generator
from ..cell import Wall
from ..models import Coordinate, Direction


class Prim(Generator):
    """Generates a maze using randomized Prim's algorithm."""

    def __call__(self, maze: mazegen.MazeGenerator, rng: Random) -> None:
        self.prim(maze, rng)

    def prim(
        self,
        maze: mazegen.MazeGenerator,
        rng: Random,
    ) -> None:
        """Function to create maze by Prim's minimal spanning tree algorithm"""

        frontiers: list[tuple[Wall, Coordinate]] = []
        visited: set[Coordinate] = {maze.entry}

        def add_frontiers(coord: Coordinate) -> None:
            x, y = coord
            cell = maze.grid[y][x]

            for direction, wall in cell.walls.items():
                if not wall.locked:
                    delta = (0, 0)
                    match direction:
                        case Direction.NORTH:
                            delta = (0, -1)
                        case Direction.EAST:
                            delta = (1, 0)
                        case Direction.SOUTH:
                            delta = (0, 1)
                        case Direction.WEST:
                            delta = (-1, 0)
                        case _:
                            assert_never(direction)

                    next_cell = Coordinate(x + delta[0], y + delta[1])
                    if next_cell not in visited:
                        frontiers.append((wall, next_cell))

        add_frontiers(maze.entry)

        while frontiers:
            frontier, coord = frontiers.pop(rng.randrange(len(frontiers)))

            if coord in visited:
                continue
            visited.add(coord)
            frontier.closed = False
            add_frontiers(coord)
