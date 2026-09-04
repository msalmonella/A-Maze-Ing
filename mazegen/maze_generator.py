"""Maze generation and solution utilities.

This module provides the ``MazeGenerator`` class for creating, modifying,
solving, rendering, and exporting mazes based on a configuration file.
"""

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
    """Generates, solves, and renders a maze."""

    grid: Grid
    _solution: Path = []
    _rng = Random()

    def __init__(self, config_path: str):
        """Initializes the maze generator from a configuration file.

        Args:
            config_path: Path to the maze configuration file.
        """

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
        """Returns the solution path.

        Returns:
            The `Path` from the maze entry to the exit.
        """

        return self._solution

    def render(self) -> None:
        """Renders the current maze with the configured renderer."""
        self.operations.renderer(self)

    def generate(self) -> Generator[None, None, None]:
        """Generates and solves the maze.

        Yields:
            None: After each generation step that produces an update.

        Returns:
            None: When maze generation is complete.
        """

        self._solution = []
        self.grid = self._initialize_grid()

        yield from self.operations.algorithm(self.grid, self.config, self._rng)
        if not self.config.perfect:
            yield from self._non_perfect()

        self._solution = self.operations.solver(self.grid, self.config)
        self._hex_writer(self.solution)

    def pattern_can_fit(self) -> bool:
        """Checks whether the 42 pattern fits inside the grid.

        Returns:
            bool: `True` if the pattern fits, otherwise `False`.
        """

        return self.config.height >= len(
            PATTERN_42
        ) and self.config.width >= len(PATTERN_42[0])

    def _non_perfect(self) -> Generator[None]:
        """Opens additional walls to create a non-perfect maze.

        Yields:
            None: Each time an additional wall is successfully opened.

        Returns:
            None: When no more walls are opened.
        """

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
        """Writes the maze and solution to the configured output file.

        Args:
            solution (Path): Path containing the solution coordinates.
        """

        config = self.config
        entry_x, entry_y = config.entry
        exit_x, exit_y = config.exit

        with open(config.output_file, "w", encoding="utf-8") as f:
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
        """Converts a coordinate path into their 'NESW' representations.

        Args:
            path (Path): `Coordinate` sequence of the solution path.

        Returns:
            list[str]: A list of directions using N, E, S, and W.
        """

        nesw: list[str] = []
        for i in range(len(path) - 1):
            current = path[i]
            next_cell = path[i + 1]

            current_x, current_y = current
            next_x, next_y = next_cell

            if next_y > current_y:
                nesw.append("S")

            if next_x > current_x:
                nesw.append("E")

            if current_y > next_y:
                nesw.append("N")

            if current_x > next_x:
                nesw.append("W")

        return nesw

    def _place_pattern_42(self, grid: Grid) -> Grid:
        """Places the permanent 42 pattern in the center of the grid.

        Ommits the pattern without raising an error if it does not fit

        Args:
            grid (Grid): Grid where the pattern should be placed.

        Returns:
            Grid: The grid with the 42 pattern cells locked.

        Raises:
            PatternError: If the pattern overlaps the entry or exit.
        """

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
                    if coord in {config.entry, config.exit}:
                        raise PatternError(
                            "Cannot place 42 pattern on entry or exit points"
                        )
        for coord in to_be_locked:
            cell = grid[coord.y][coord.x]
            cell.lock()
        return grid

    def _initialize_grid(self) -> Grid:
        """Creates the initial maze grid with shared walls in the closed state.

        Returns:
            Grid: A newly initialized maze grid.
        """

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
