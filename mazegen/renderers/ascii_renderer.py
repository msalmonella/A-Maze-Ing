import curses
from enum import Enum, StrEnum
import mazegen
from . import Renderer, Colors
from ..cell import Cell as MazeCell
from ..models import Path, Direction


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
        self,
        cell: MazeCell,
        maze: mazegen.MazeGenerator,
        solution: Path,
        x,
        y,
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
    def __init__(self, renderer: type[Renderer], stdscr: curses.window):
        self.renderer = renderer
        self.stdscr = stdscr
        self.running = True
        self.menu_index = 0
        self.regenerate = True
        self.show_solution = False
        self.show_solution_trigger = False

    def on_quit(self) -> None:
        self.running = False

    def on_regen(self) -> None:
        self.regenerate = True

    def on_show(self) -> None:
        self.show_solution_trigger = True

    class Option(StrEnum):
        SHOW = "Toggle Solution"
        RECREATE = "Recreate"
        QUIT = "Quit"

    actions = {
        Option.QUIT: on_quit,
        Option.RECREATE: on_regen,
        Option.SHOW: on_show,
    }

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
                        maze_cell,
                        maze,
                        solution,
                        x_value,
                        y_value,
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

        options = list(self.Option)
        for i, option in enumerate(options):
            prefix = "> " if i == self.menu_index else "  "
            suffix = (
                ": " + ("Hidden", "Visible")[self.show_solution]
                if option == self.Option.SHOW
                else ""
            )
            try:
                self.stdscr.addstr(y + i, 0, prefix + option + suffix)
            except curses.error:
                pass

        self.stdscr.refresh()

    def handle_input(self, key: int):
        if key == curses.KEY_UP:
            self.menu_index -= 1
        elif key == curses.KEY_DOWN:
            self.menu_index += 1
        elif key in (10, 13, curses.KEY_ENTER):
            self.select()

        self.menu_index %= len(self.Option)

    def select(self):
        options = list(self.Option)
        option = options[self.menu_index]
        action = self.actions[option]
        action(self)


class AsciiRenderer(Renderer):
    def __call__(self, maze: mazegen.MazeGenerator) -> None:
        curses.wrapper(self.main, maze)

    def main(self, stdscr: curses.window, maze: mazegen.MazeGenerator) -> None:
        Colors.init_pairs()
        curses.curs_set(0)
        # stdscr.keypad(True)
        stdscr.timeout(round(1000 / maze.sps))

        ascii_view = Ascii(Renderer, stdscr)

        while ascii_view.regenerate:
            ascii_view.regenerate = False
            generation = maze.generate()
            generating = True

            while ascii_view.running:
                if ascii_view.show_solution_trigger:
                    ascii_view.show_solution = not ascii_view.show_solution
                    ascii_view.show_solution_trigger = False
                    # stdscr.clear()

                if generating:
                    try:
                        next(generation)
                    except StopIteration:
                        generating = False

                ascii_view.draw(maze, maze.solution, ascii_view.show_solution)
                key = stdscr.getch()
                ascii_view.handle_input(key)

                if ascii_view.regenerate:
                    break
