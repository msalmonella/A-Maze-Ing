import sys
from random import Random
import mazegen
from . import Algorithm
from ..models import Coordinate, Direction
from ..errors import LockedWallError


class MazerTheMiner(Algorithm):

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

        x, y = head
        cell = maze.grid[y][x]
        processed.add(head)

        directions = list(Direction)
        rng.shuffle(directions)

        for direction in directions:
            next_index = cell.neighbor(direction)

            if next_index not in processed:
                try:
                    wall = cell.walls[direction]
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
