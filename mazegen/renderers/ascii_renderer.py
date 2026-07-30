import mazegen
import os
from . import Renderer
from ..models import Path
from enum import  StrEnum

terminal_size = os.get_terminal_size()


class Cell(StrEnum):
    DEBUG = "+"
    SPACE = " " * 2
    class Wall(StrEnum):
        HORIZONTAL = "=" * 3
        VERTICAL = "|"

def clear_space(maze: mazegen.MazeGenerator) -> None:
    """Responsible for clearing up the buffer"""
    for _ in range(terminal_size.columns):
        for _ in range(terminal_size.lines):
            print(Cell.SPACE, end="")


class AsciiRenderer(Renderer):
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:

        print("\033[H", end="")
        clear_space(maze)
        print("\033[H", end="")
        for _ in range(maze.width):
            print(Cell.Wall.HORIZONTAL, end="")
        print("=", end="")
        print()
        for y in maze.grid:
            print(Cell.Wall.VERTICAL, end="")
            for x in y:
                print(Cell.SPACE, end="")
                print(Cell.Wall.VERTICAL, end="")
            print()
            print("=", end="")
            for x in y:
                print(Cell.Wall.HORIZONTAL, end="")
            print("")

