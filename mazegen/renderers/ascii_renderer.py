import curses
import mazegen
from . import Renderer, Colors
from ..cell import Cell as MazeCell
from ..models import Path, Direction
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
    SOLUTION_PATH = (4, "█")


GLYPH_COLORS: dict[Glyph, Colors] = {
    Glyph.EXIT_POINT: Colors.RED,
    Glyph.ENTRY_POINT: Colors.GREEN,
    Glyph.SOLUTION_PATH: Colors.YELLOW,
}


class CellSprite:
    """Renders a single maze cell's sprite, respecting open/closed walls."""

    def __init__(self, width: int = 1, height: int = 1):
        self.width = width * 3
        self.height = height

    def along_the_way(self, x: int, y: int, solution: Path) -> bool:
        for i in solution:
            if (x, y) == (i.x, i.y):
                return True
        return False

    def exit_condition(
        self, x: int, y: int, maze: mazegen.MazeGenerator
    ) -> bool:
        if (x, y) == maze.exit:
            return True
        return False

    def entry_condition(
        self, x: int, y: int, maze: mazegen.MazeGenerator
    ) -> bool:
        if (x, y) == maze.entry:
            return True
        return False

    def sprite(
        self, cell: MazeCell,
        maze: mazegen.MazeGenerator,
        solution: Path,
        x, y,
        show_solution: bool,
    ) -> list[list[Glyph]]:
        rows: list[list[Glyph]] = []

        north_glyph = (
            Glyph.WALL if cell.walls[Direction.NORTH].closed else Glyph.SPACE
        )
        rows.append([Glyph.WALL] + [north_glyph] * self.width + [Glyph.WALL])

        west_glyph = (
            Glyph.WALL if cell.walls[Direction.WEST].closed else Glyph.SPACE
        )
        east_glyph = (
            Glyph.WALL if cell.walls[Direction.EAST].closed else Glyph.SPACE
        )
        for _ in range(self.height):
            if self.exit_condition(x, y, maze):
                mid = Glyph.EXIT_POINT
            elif self.entry_condition(x, y, maze):
                mid = Glyph.ENTRY_POINT
            elif self.along_the_way(x, y, solution):
                if show_solution:
                    mid = Glyph.SOLUTION_PATH
                else:
                    mid = Glyph.SPACE
            else:
                mid = Glyph.SPACE

            rows.append([west_glyph] + [mid] * self.width + [east_glyph])

        south_glyph = (
            Glyph.WALL if cell.walls[Direction.SOUTH].closed else Glyph.SPACE
        )
        rows.append([Glyph.WALL] + [south_glyph] * self.width + [Glyph.WALL])

        return rows


class Ascii:
    def __init__(self, renderer, stdscr):
        self.renderer = renderer
        self.stdscr = stdscr
        self.running = True
        self.menu_index = 0
        self.regenerate = False
        self.show_solution = False
        self.show_solution_trigger = False

    def _menu_items(self) -> list[str]:
        return [
            "Show Solution: YES" if self.show_solution else "Show Solution: NO",
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

    def draw(
        self,
        maze: mazegen.MazeGenerator,
        solution: Path,
        show_solution: bool,
    ) -> None:
        self.stdscr.erase()
        cell_sprite = CellSprite(1, 1)

        y = 0

        for y_value in range(maze.height):
            row_cells = []
            for x_value in range(maze.width):
                maze_cell = maze.grid[y_value][x_value]
                row_cells.append(
                    cell_sprite.sprite(
                        maze_cell, maze, solution, x_value, y_value,
                        show_solution,
                    )
                )

            for line_parts in zip(*row_cells):
                line: list[Glyph] = []
                for part in line_parts:
                    line.extend(part)
                self._draw_line(y, 0, line)
                y += 1

        # draw the menu underneath
        y += 1

        menu = self._menu_items()
        for i, item in enumerate(menu):
            prefix = "> " if i == self.menu_index else "  "
            try:
                self.stdscr.addstr(y + i, 0, prefix + item)
            except curses.error:
                pass

        self.stdscr.refresh()

    def handle_input(self, key):
        menu = self._menu_items()
        if key == curses.KEY_UP:
            self.menu_index -= 1
        elif key == curses.KEY_DOWN:
            self.menu_index += 1
        elif key in (10, 13, curses.KEY_ENTER):
            self.select()

        self.menu_index %= len(menu)

    def select(self):
        menu = self._menu_items()
        choice = menu[self.menu_index]
        if choice == "Quit":
            self.running = False
        elif choice == "Recreate Maze":
            self.regenerate = True
        elif choice.startswith("Show Solution"):
            self.show_solution_trigger = True


def main(stdscr: curses.window, maze: mazegen.MazeGenerator):
    Colors.init_pairs()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.timeout(round(1000 / maze.sps))

    ascii_view = Ascii(Renderer, stdscr)

    generation = maze.generate()
    generating = True
    solution = []

    while ascii_view.running:
        if ascii_view.show_solution_trigger:
            ascii_view.show_solution = not ascii_view.show_solution
            ascii_view.show_solution_trigger = False
            stdscr.clear()

        if generating:
            try:
                next(generation)
            except StopIteration:
                generating = False
                solution = maze.solve()
        ascii_view.draw(maze, solution, ascii_view.show_solution)
        key = stdscr.getch()
        ascii_view.handle_input(key)

        if ascii_view.regenerate:
            generation = maze.generate()
            generating = True
            solution = []
            ascii_view.regenerate = False


class AsciiRenderer(Renderer):
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        curses.wrapper(main, maze)
