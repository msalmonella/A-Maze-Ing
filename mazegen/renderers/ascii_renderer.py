import mazegen
import os
from . import Renderer
from ..models import Path
from enum import  StrEnum

terminal_size = os.get_terminal_size()

class Glyph(StrEnum):
    EDGE = "+"
    SPACE = " "
    H_WALL = "—"
    V_WALL = "|"

class Cell:
    def __init__(self, width: int = 3, height: int = 3):
        self.width = width * 3 #for making the cell look prettier
        self.height = height

    def sprite(self) -> list[str]:
        rows = []

        rows.append(Glyph.EDGE + Glyph.H_WALL * self.width + Glyph.EDGE)

        for _ in range(self.height):
            rows.append(Glyph.V_WALL + Glyph.SPACE * self.width + Glyph.V_WALL)

        rows.append(Glyph.EDGE + Glyph.H_WALL * self.width + Glyph.EDGE)

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
        # this is for testing purposes ===========
        cell = Cell(1, 1)
        clear_space(maze)
        # this is for testing purposes ===========
        for _ in range(maze.width):
            for _ in cell.sprite():
                print(_ * maze.height)

