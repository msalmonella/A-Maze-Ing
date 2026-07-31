import mazegen
import os
from . import Renderer
from ..cell import Cell as MazeCell
from ..models import Path
from enum import StrEnum

terminal_size = os.get_terminal_size()


class Glyph(StrEnum):
    EDGE = "+"
    SPACE = " "
    H_WALL = "—"
    V_WALL = "|"


class CellSprite:
    """Renders a single maze cell's sprite, respecting open/closed walls."""

    def __init__(self, width: int = 1, height: int = 1):
        self.width = width * 3
        self.height = height

    def sprite(self, cell: MazeCell) -> list[str]:
        rows = []

        north_glyph = Glyph.H_WALL if cell.north.closed else Glyph.SPACE
        rows.append(Glyph.EDGE + north_glyph * self.width + Glyph.EDGE)

        west_glyph = Glyph.V_WALL if cell.west.closed else Glyph.SPACE
        east_glyph = Glyph.V_WALL if cell.east.closed else Glyph.SPACE
        for _ in range(self.height):
            rows.append(west_glyph + Glyph.SPACE * self.width + east_glyph)

        south_glyph = Glyph.H_WALL if cell.south.closed else Glyph.SPACE
        rows.append(Glyph.EDGE + south_glyph * self.width + Glyph.EDGE)

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
                row_cells.append(cell_sprite.sprite(maze_cell))

            for line_parts in zip(*row_cells):
                print("".join(line_parts))
