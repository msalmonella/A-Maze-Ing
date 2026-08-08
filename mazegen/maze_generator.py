from random import Random
from .cell import Cell
from .models import Path

Grid = list[list[Cell]]


class MazeGenerator:
    grid: Grid
    _rng = Random()

    def __init__(self, config_path: str):
        from .config import parse_config

        cfg = parse_config(config_path)

        self.width = cfg.width
        self.height = cfg.height
        self.entry = cfg.entry
        self.exit = cfg.exit
        self.output_file = cfg.output_file
        self.perfect = cfg.perfect

        self.seed = cfg.seed
        self.generator = cfg.generator()
        self.solver = cfg.solver()
        self.renderer = cfg.renderer()

        self._rng.seed(self.seed if self.seed else None)
        self.generate()

    def __repr__(self) -> str:
        return "\n".join(
            " ".join(f"{cell.value:2}" for cell in row) for row in self.grid
        )

    def render(self) -> None:
        self.renderer(self, self.solver(self))

    def solve(self) -> Path:
        return self.solver(self)

    def generate(self) -> None:
        self.grid = self._initialize_grid()
        self.generator(self, self._rng)
        self._hex_writer(self.solver(self))

    def _hex_writer(self, solution: Path) -> None:
        """writes in text format"""
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        with open(self.output_file, "w") as f:
            print(self.output_file)
            for row in self.grid:
                line = ""
                for cell in row:
                    line += hex(cell.value)[2:]
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{entry_x},{entry_y}\n")
            f.write(f"{exit_x},{exit_y}\n")
            f.write(f"{"".join(self._nesw_conversion(solution))}")

    def _nesw_conversion(self, path: Path) -> list[str]:
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

    def _pattern_42(self, grid: Grid) -> Grid:
        """Places permanent 42 pattern if fits into the grid"""

        pattern = [
            "X   XXX",
            "X     X",
            "XXX XXX",
            "  X X  ",
            "  X XXX",
        ]
        padding = 1

        if (
            self.height < len(pattern) + padding * 2
            or self.width < len(pattern[0]) + padding * 2
        ):
            return grid

        for y, line in enumerate(pattern):
            offset_y = (self.height - len(pattern)) // 2
            offset_x = (self.width - len(line)) // 2

            for x, char in enumerate(line):
                cell = grid[y + offset_y][x + offset_x]
                if char == "X":
                    cell.lock()
        return grid

    def _initialize_grid(self) -> Grid:
        """Generate the initial maze grid with shared closed walls."""
        grid: Grid = []

        for row in range(self.height):
            grid.append([])

            for column in range(self.width):
                wall_above = grid[row - 1][column].south if row else None
                wall_before = grid[row][column - 1].east if column else None

                if wall_above:
                    wall_above.locked = False
                if wall_before:
                    wall_before.locked = False

                grid[row].append(Cell(north=wall_above, west=wall_before))

        return self._pattern_42(grid)
