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

    def render(self, solution: Path) -> None:
        self.renderer(self, solution)

    def solve(self) -> Path:
        return self.solver(self)

    def generate(self, seed: str = "") -> None:
        self.generator(self, seed=seed)

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
