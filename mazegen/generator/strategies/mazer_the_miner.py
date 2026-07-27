import mazegen
from . import Strategy
from ..cell import Wall
from ..models import GridIndex, Direction
from ..seeder import seed_generator


class MazerTheMiner(Strategy):

    def __call__(self, maze: mazegen.MazeGenerator, seed: str = "") -> None:
        self.mazer_the_miner(maze, seed)

    def mazer_the_miner(
        self,
        maze: mazegen.MazeGenerator,
        seed: str = "",
        head: GridIndex = GridIndex(0, 0),
        processed: set[GridIndex] = set(),
    ) -> None:
        """Recursive function to create maze by digging into walls"""
        processed.add(head)
        rng = seed_generator(seed)
        directions = [d.value for d in Direction]

        rng.shuffle(directions)
        for direction in directions:
            next_index: GridIndex
            match direction:
                case Direction.NORTH:
                    next_index = GridIndex(head.row - 1, head.column)
                case Direction.EAST:
                    next_index = GridIndex(head.row, head.column + 1)
                case Direction.SOUTH:
                    next_index = GridIndex(head.row + 1, head.column)
                case Direction.WEST:
                    next_index = GridIndex(head.row, head.column - 1)
                case _:
                    raise Exception

            if (
                0 <= next_index.column < maze.width
                and 0 <= next_index.row < maze.height
                and not next_index in processed
            ):
                row, column = head

                wall: Wall
                match direction:
                    case Direction.NORTH:
                        wall = maze.grid[row][column].north
                    case Direction.EAST:
                        wall = maze.grid[row][column].east
                    case Direction.SOUTH:
                        wall = maze.grid[row][column].south
                    case Direction.WEST:
                        wall = maze.grid[row][column].west
                    case _:
                        raise Exception
                wall.closed = False

                self.mazer_the_miner(maze, seed, next_index, processed)
