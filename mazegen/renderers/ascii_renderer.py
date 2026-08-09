import curses
import mazegen
from . import Renderer, Colors
from ..cell import Cell as MazeCell
from ..models import Path
from enum import Enum


class Glyph(Enum):

    char: str

    def __new__(cls, glyph_id: int, char: str):
        obj = object.__new__(cls)
        obj._value_ = glyph_id
        obj.char = char
        return obj

    SPACE = (0, " ")
    WALL = (1, "█")
    EXIT_POINT = (2, "█")
    ENTRY_POINT = (3, "█")


GLYPH_COLORS: dict[Glyph, Colors] = {
    Glyph.EXIT_POINT: Colors.RED,
    Glyph.ENTRY_POINT: Colors.GREEN,
}


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
    ) -> list[list[Glyph]]:
        rows: list[list[Glyph]] = []

        north_glyph = Glyph.WALL if cell.north.closed else Glyph.SPACE
        rows.append([Glyph.WALL] + [north_glyph] * self.width + [Glyph.WALL])

        west_glyph = Glyph.WALL if cell.west.closed else Glyph.SPACE
        east_glyph = Glyph.WALL if cell.east.closed else Glyph.SPACE
        for _ in range(self.height):
            if self.exit_condition(x, y, maze):
                mid = Glyph.EXIT_POINT
            elif self.entry_condition(x, y, maze):
                mid = Glyph.ENTRY_POINT
            else:
                mid = Glyph.SPACE

            rows.append([west_glyph] + [mid] * self.width + [east_glyph])

        south_glyph = Glyph.WALL if cell.south.closed else Glyph.SPACE
        rows.append([Glyph.WALL] + [south_glyph] * self.width + [Glyph.WALL])

        return rows


class Ascii:
    def __init__(self, renderer, stdscr):
        self.renderer = renderer
        self.stdscr = stdscr
        self.running = True
        self.menu_index = 0

        self.menu = [
            "Recreate Maze",
            "Quit",
        ]

    def _draw_line(self, y: int, x: int, glyphs: list[Glyph]) -> None:
        stdscr = self.stdscr
        col = x
        i = 0
        n = len(glyphs)
        while i < n:
            member = glyphs[i]
            color = GLYPH_COLORS.get(member)
            j = i + 1
            while j < n and glyphs[j] is member:
                j += 1
            chunk = member.char * (j - i)
            try:
                if color is not None:
                    stdscr.addstr(y, col, chunk, color.pair)
                else:
                    stdscr.addstr(y, col, chunk)
            except curses.error:
                pass
            col += len(chunk)
            i = j

    def draw(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        self.stdscr.erase()
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
                line: list[Glyph] = []
                for part in line_parts:
                    line.extend(part)
                self._draw_line(y, 0, line)
                y += 1

        # draw the menu underneath
        y += 1

        for i, item in enumerate(self.menu):
            prefix = "> " if i == self.menu_index else "  "
            try:
                self.stdscr.addstr(y + i, 0, prefix + item)
            except curses.error:
                pass

        self.stdscr.refresh()

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
        elif self.menu[self.menu_index] == "Recreate":
            pass


def main(stdscr, maze: mazegen.MazeGenerator, solution: Path):
    Colors.init_pairs()
    curses.curs_set(0)
    stdscr.keypad(True)

    ascii_view = Ascii(Renderer, stdscr)

    while ascii_view.running:
        ascii_view.draw(maze, solution)

        key = stdscr.getch()

        ascii_view.handle_input(key)


class AsciiRenderer(Renderer):
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        # curses.wrapper(main, maze, solution)
        print(solution)
