import os
import curses
import mazegen
from . import Renderer, Colors
from ..cell import Cell as MazeCell
from ..models import Path
from enum import StrEnum

stdscr = curses.initscr()
terminal_size = os.get_terminal_size()
RED = Colors.RED
GREEN = Colors.GREEN
RESET = Colors.RESET

class Glyph(StrEnum):
    SPACE = " "
    WALL = "█"
    EXIT_POINT = f"{RED}█{RESET}"
    ENTRY_POINT = f"{GREEN}█{RESET}"
    # EXIT_POINT = f"X"
    # ENTRY_POINT = f"@"


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
    stdscr.move(0, 0)
    for _ in range(terminal_size.columns):
        for _ in range(terminal_size.lines):
            print(Glyph.SPACE, end="")
    stdscr.move(0, 0)


class Ascii:

    def __init__(self, renderer):
        self.renderer = renderer
        self.running = True
        self.menu_index = 0

        self.menu = [
            "Recreate Maze",
            "Quit"
        ]

    def draw(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        stdscr.clear()
        cell_sprite = CellSprite(1, 1)

        y = 0

        for y_value in range(maze.height):
            row_cells = []
            for x_value in range(maze.width):
                maze_cell = maze.grid[y_value][x_value]
                row_cells.append(
                    cell_sprite.sprite(maze_cell, maze, solution, x_value, y_value)
                )

            for line_parts in zip(*row_cells):
                line = "".join(line_parts)
                try:
                    stdscr.addstr(y, 0, line)
                except curses.error:
                    pass
                y += 1

        # draw the menu underneath
        y += 1

        for i, item in enumerate(self.menu):
            prefix = "> " if i == self.menu_index else "  "
            try:
                stdscr.addstr(y + i, 0, prefix + item)
            except curses.error:
                pass

        stdscr.refresh()

    def handle_input(self, key):

        if key == curses.KEY_UP:
            self.menu_index -= 1

        elif key == curses.KEY_DOWN:
            self.menu_index += 1

        elif key in (10, 13, curses.KEY_ENTER):
            self.select()


        self.menu_index %= len(self.menu)

    def select(self):

        if self.menu[self.menu_index] == "Quit":
            self.running = False

def main(stdscr, maze: mazegen.MazeGenerator, solution: Path):

    curses.curs_set(0)
    stdscr.keypad(True)

    ascii = Ascii(Renderer)

    while ascii.running:
        ascii.draw(maze, solution)

        key = stdscr.getch()

        ascii.handle_input(key)

class AsciiRenderer(Renderer):
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        curses.wrapper(main, maze, solution)
