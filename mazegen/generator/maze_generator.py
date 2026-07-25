from typing import NamedTuple
from .config_parser import parse_config
from .cell import Direction, Wall, Cell
from .seeder import seed_generator

Grid = list[list[Cell]]


class GridIndex(NamedTuple):
    row: int
    column: int


class MazeGenerator:
    grid: Grid

    def __init__(self, config_path: str):
        cfg = parse_config(config_path)

        self.width = cfg["width"]
        self.height = cfg["height"]
        self.entry = cfg["entry"]
        self.exit = cfg["exit"]
        self.output_file = cfg["output_file"]
        self.perfect = cfg["perfect"]

        self.grid = self._generate_grid()

    def _mazer_the_miner(
        self,
        head: GridIndex = GridIndex(0, 0),
        processed: set[GridIndex] = set(),
        seed: str = "",
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
                0 <= next_index.column < self.width
                and 0 <= next_index.row < self.height
                and not next_index in processed
            ):
                row, column = head

                wall: Wall
                match direction:
                    case Direction.NORTH:
                        wall = self.grid[row][column].north
                    case Direction.EAST:
                        wall = self.grid[row][column].east
                    case Direction.SOUTH:
                        wall = self.grid[row][column].south
                    case Direction.WEST:
                        wall = self.grid[row][column].west
                    case _:
                        raise Exception
                wall.closed = False

                self._mazer_the_miner(next_index, processed, seed)

    def generate_maze(self, seed: str = "") -> None:
        self._mazer_the_miner(seed=seed)

    def _generate_grid(self) -> Grid:
        """Generate the initial maze grid with shared closed walls."""
        grid: Grid = []

        for row in range(self.height):
            grid.append([])

            for column in range(self.width):
                above = grid[row - 1][column] if row else None
                before = grid[row][column - 1] if column else None

                grid[row].append(
                    Cell(
                        north=above.south if above else None,
                        west=before.east if before else None,
                    )
                )

        return grid
