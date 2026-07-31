import mazegen
from . import Generator
from ..cell import Wall
from ..models import Coordinate, Direction
from ..seeder import seed_generator


class MazerTheMiner(Generator):

    def __call__(self, maze: mazegen.MazeGenerator, seed: str = "") -> None:
        rng = seed_generator(seed)
        self.mazer_the_miner(maze, rng, Coordinate(0, 0), set())

    def mazer_the_miner(
        self,
        maze: mazegen.MazeGenerator,
        rng: random.Random,
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

            if (
                0 <= next_index.x < maze.width
                and 0 <= next_index.y < maze.height
                and next_index not in processed
            ):
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

                self.mazer_the_miner(maze, rng, next_index, processed)
