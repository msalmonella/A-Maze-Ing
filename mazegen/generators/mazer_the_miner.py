import mazegen
from . import Generator
from ..cell import Wall
from ..models import Coordinate, Direction
from ..errors import LockedWallError
from random import Random
import sys


class MazerTheMiner(Generator):

    def __call__(self, maze: mazegen.MazeGenerator, rng: Random) -> None:
        self._apply_recursion_limit(maze.width, maze.height)
        self.mazer_the_miner(maze, rng, Coordinate(0, 0), set())

    def mazer_the_miner(
        self,
        maze: mazegen.MazeGenerator,
        rng: Random,
        head: Coordinate,
        processed: set[Coordinate],
    ) -> None:
        """Recursive function to create maze by digging into walls"""
        processed.add(head)
        directions = [d.value for d in Direction]
        rng.shuffle(directions)

        for direction in directions:
            next_index: Coordinate
            match direction:
                case Direction.NORTH:
                    next_index = Coordinate(head.x, head.y - 1)
                case Direction.EAST:
                    next_index = Coordinate(head.x + 1, head.y)
                case Direction.SOUTH:
                    next_index = Coordinate(head.x, head.y + 1)
                case Direction.WEST:
                    next_index = Coordinate(head.x - 1, head.y)
                case _:
                    raise Exception

            if next_index not in processed:
                try:
                    x, y = head

                    wall: Wall
                    match direction:
                        case Direction.NORTH:
                            wall = maze.grid[y][x].north
                        case Direction.EAST:
                            wall = maze.grid[y][x].east
                        case Direction.SOUTH:
                            wall = maze.grid[y][x].south
                        case Direction.WEST:
                            wall = maze.grid[y][x].west
                        case _:
                            raise Exception
                    wall.closed = False
                except LockedWallError:
                    continue

                self.mazer_the_miner(maze, rng, next_index, processed)

    @staticmethod
    def _apply_recursion_limit(width: int, height: int) -> None:
        cell_count = width * height
        wall_count = 4
        needed = cell_count * wall_count
        if needed > sys.getrecursionlimit():
            sys.setrecursionlimit(needed)
