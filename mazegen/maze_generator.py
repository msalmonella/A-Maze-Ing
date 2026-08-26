from random import Random
from collections.abc import Generator
from .cell import Cell, Grid
from .models import Path, Coordinate, Direction
from .errors import PatternError, LockedWallError

PATTERN_42 = [
    "         ",
    " X   XXX ",
    " X     X ",
    " XXX XXX ",
    "   X X   ",
    "   X XXX ",
    "         ",
]


class MazeGenerator:
    grid: Grid
    _solution: Path = []
    _rng = Random()

    def __init__(self, config_path: str):
        from .config import parse_config

        cfg = parse_config(config_path)

        self.config = cfg.mandatory
        self.operations = cfg.operations

        self.seed = cfg.seed
        self.sps = cfg.sps

        self._rng.seed(self.seed if self.seed else None)
        self.grid = self._initialize_grid()

    def __repr__(self) -> str:
        return "\n".join(
            " ".join(f"{cell.value:2}" for cell in row) for row in self.grid
        )

    @property
    def solution(self) -> Path:
        return self._solution

    def render(self) -> None:
        self.operations.renderer(self)

    def generate(self) -> Generator[None, None, None]:
        self._solution = []
        self.grid = self._initialize_grid()

        yield from self.operations.algorithm(self.grid, self.config, self._rng)
        if not self.config.perfect:
            yield from self._non_perfect()

        self._solution = self.operations.solver(self.grid, self.config)
        self._hex_writer(self.solution)

    def pattern_can_fit(self) -> bool:
        return self.config.height >= len(
            PATTERN_42
        ) and self.config.width >= len(PATTERN_42[0])

    def _non_perfect(self) -> Generator[None]:
        for row in self.grid:
            for cell in row:
                if cell.value.bit_count() == 3:
                    walls = list(cell.walls.values())
                    shifted = walls[1:] + walls[:1]
                    for wall in shifted:
                        if wall.closed:
                            try:
                                wall.closed = False
                            except LockedWallError:
                                continue
                            else:
                                yield
                                break

    def _hex_writer(self, solution: Path) -> None:
        """writes in text format"""
        config = self.config
        entry_x, entry_y = config.entry
        exit_x, exit_y = config.exit

        with open(config.output_file, "w") as f:
            # print(self.output_file)
            for row in self.grid:
                line = ""
                for cell in row:
                    line += hex(cell.value)[2:]
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{entry_x},{entry_y}\n")
            f.write(f"{exit_x},{exit_y}\n")
            f.write(f"{"".join(self._nesw_conversion(solution))}")

    @staticmethod
    def _nesw_conversion(path: Path) -> list[str]:
        """Converts to NESW text format"""
        nesw: list[str] = []
        for i in range(len(path) - 1):
            current = path[i]
            next_cell = path[i + 1]

            current_x, current_y = current
            next_x, next_y = next_cell

            if next_y > current_y:
                nesw.append("N")

            if next_x > current_x:
                nesw.append("E")

            if current_y > next_y:
                nesw.append("S")

            if current_x > next_x:
                nesw.append("W")

        return nesw

    def _place_pattern_42(self, grid: Grid) -> Grid:
        """Places permanent 42 pattern if fits into the grid"""
        config = self.config

        if not self.pattern_can_fit():
            return grid

        to_be_locked: list[Coordinate] = []

        for y, line in enumerate(PATTERN_42):
            offset_y = (config.height - len(PATTERN_42)) // 2
            offset_x = (config.width - len(line)) // 2

            for x, char in enumerate(line):
                if char == "X":
                    coord = Coordinate(x + offset_x, y + offset_y)
                    to_be_locked.append(coord)
                    if coord == config.entry or coord == config.exit:
                        raise PatternError(
                            "Cannot place 42 pattern on entry or exit points"
                        )
        for coord in to_be_locked:
            cell = grid[coord.y][coord.x]
            cell.lock()
        return grid

    def _initialize_grid(self) -> Grid:
        """Generate the initial maze grid with shared closed walls."""
        grid: Grid = []

        for row in range(self.config.height):
            grid.append([])

            for column in range(self.config.width):
                wall_above = (
                    grid[row - 1][column].walls[Direction.SOUTH]
                    if row
                    else None
                )
                wall_before = (
                    grid[row][column - 1].walls[Direction.EAST]
                    if column
                    else None
                )

                if wall_above:
                    wall_above.locked = False
                if wall_before:
                    wall_before.locked = False

                grid[row].append(
                    Cell(
                        Coordinate(column, row),
                        north=wall_above,
                        west=wall_before,
                    )
                )

        return self._place_pattern_42(grid)
