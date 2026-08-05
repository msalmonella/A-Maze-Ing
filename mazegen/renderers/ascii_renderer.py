import os
import mazegen
from . import Renderer, Colors
from ..cell import Cell as MazeCell
from ..models import Path, Coordinate
from enum import StrEnum

terminal_size = os.get_terminal_size()
RED = Colors.RED
GREEN = Colors.GREEN
RESET = Colors.RESET

class Glyph(StrEnum):
    SPACE = " "
    WALL = "█"
    EXIT_POINT = f"{RED}█{RESET}"
    ENTRY_POINT = f"{GREEN}█{RESET}"


class CellSprite:
    """Renders a single maze cell's sprite, respecting open/closed walls."""

    def __init__(self, width: int = 1, height: int = 1):
        self.width = width * 3
        self.height = height

    def exit_condition(self, x: int, y: int, maze: mazegen.MazeGenerator) -> bool:
        exit_x, exit_y = maze.exit
        comparison: tuple[int, int] = x, y
        if comparison == (exit_x, exit_y):
            return True
        return False

    def entry_condition(self, x: int, y: int, maze: mazegen.MazeGenerator) -> bool:
        entry_x, entry_y = maze.entry
        comparison: tuple[int, int] = x, y
        if comparison == (entry_x, entry_y):
            return True
        return False

    def sprite(
        self, cell: MazeCell, maze: mazegen.MazeGenerator, solution: Path, x, y
    ) -> list[str]:
        rows = []

        north_glyph = Glyph.WALL if cell.north.closed else Glyph.SPACE
        rows.append(Glyph.WALL + north_glyph * self.width + Glyph.WALL)

        west_glyph = Glyph.WALL if cell.west.closed else Glyph.SPACE
        east_glyph = Glyph.WALL if cell.east.closed else Glyph.SPACE
        for _ in range(self.height):
            rows.append(
                west_glyph
                + (
                    Glyph.EXIT_POINT
                    if self.exit_condition(x, y, maze)
                    else (
                        Glyph.ENTRY_POINT
                        if self.entry_condition(x, y, maze)
                        else Glyph.SPACE
                    )
                )
                * self.width
                + east_glyph
            )

        south_glyph = Glyph.WALL if cell.south.closed else Glyph.SPACE
        rows.append(Glyph.WALL + south_glyph * self.width + Glyph.WALL)

        return rows


def clear_space(maze: mazegen.MazeGenerator) -> None:
    """Responsible for clearing up the buffer"""
    print("\033[H", end="")
    for _ in range(terminal_size.columns):
        for _ in range(terminal_size.lines):
            print(Glyph.SPACE, end="")
    print("\033[H", end="")


class AsciiRenderer(Renderer):
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        cell_sprite = CellSprite(1, 1)
        clear_space(maze)

        for y_value in range(maze.height):
            row_cells = []
            for x_value in range(maze.width):
                maze_cell = maze.grid[y_value][x_value]
                row_cells.append(
                    cell_sprite.sprite(maze_cell, maze, solution, x_value, y_value)
                )

            for line_parts in zip(*row_cells):
                print("".join(line_parts))
