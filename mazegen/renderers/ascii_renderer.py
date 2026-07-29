import mazegen
from . import Renderer
from ..models import Path
from enum import  StrEnum

class Cell(StrEnum):
    SPACE = " " * 2
    class Wall(StrEnum):
        HORIZONTAL = "=" * 3
        VERTICAL = "|"

class AsciiRenderer(Renderer):
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
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

