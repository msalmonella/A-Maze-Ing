from .config_parser import parse_config
from .cell import Cell
from .strategies import Strategy, MazerTheMiner

Grid = list[list[Cell]]


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

    def generate_maze(
        self, strategy: Strategy = MazerTheMiner(), seed: str = ""
    ) -> None:
        strategy(self, seed=seed)

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
