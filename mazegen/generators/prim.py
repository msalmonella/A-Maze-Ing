from random import Random
from typing import assert_never
import mazegen
from . import Generator
from ..cell import Wall
from ..models import Coordinate, Direction


class Prim(Generator):

    def __call__(self, maze: mazegen.MazeGenerator, rng: Random) -> None:
        self.prim(maze, rng)

    def prim(
        self,
        maze: mazegen.MazeGenerator,
        rng: Random,
    ) -> None:
        """Function to create maze by Prim's minimal spanning tree algorithm"""

        frontiers: dict[Coordinate, Wall | None] = {maze.entry: None}
        visited: set[Coordinate] = set()

        while frontiers:
            frontier, door = list(frontiers.items())[
                rng.randrange(len(frontiers))
            ]
            del frontiers[frontier]

            x, y = frontier
            cell = maze.grid[y][x]

            if door:
                door.closed = False

            visited.add(frontier)

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
                        frontiers.setdefault(next_cell, wall)
