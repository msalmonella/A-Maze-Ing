from .cell import Cell
from .models import Path

Grid = list[list[Cell]]


class MazeGenerator:
    grid: Grid

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

        self.grid = self._generate_grid()

    def __repr__(self) -> str:
        return "\n".join(
            " ".join(f"{cell.value:2}" for cell in row) for row in self.grid
        )

    def render(self, solution: Path) -> None:
        self.renderer(self, solution)

    def solve(self) -> Path:
        return self.solver(self)

    def generate(self, seed: str = "") -> None:
        self.generator(self, seed=seed)

    def _pattern_42(self, grid: Grid):
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

    def _generate_grid(self) -> Grid:
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
