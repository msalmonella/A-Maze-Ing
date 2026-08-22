import curses
from enum import Enum, StrEnum
from functools import reduce
from dataclasses import dataclass
import mazegen
from . import Renderer, Colors
from ..cell import Cell
from ..models import Direction, Coordinate


class Glyph(Enum):
    SPACE = (" ", 0)
    CORNER = ("•", 1)

    HORIZONTAL = ("━", 2)
    VERTICAL = ("┃", 3)

    ENTRY = ("█", 4)
    EXIT = ("█", 5)

    SOLUTION = ("█", 6)
    PATTERN = ("█", 7)

    @property
    def color(self) -> Colors | None:
        return {
            Glyph.HORIZONTAL: Colors.WHITE,
            Glyph.VERTICAL: Colors.WHITE,
            Glyph.EXIT: Colors.RED,
            Glyph.ENTRY: Colors.GREEN,
            Glyph.SOLUTION: Colors.YELLOW,
        }.get(self)


@dataclass(frozen=True)
class Sprite:
    """The representation of a single maze cell."""

    north: Glyph
    west: Glyph
    south: Glyph
    east: Glyph
    center: Glyph

    location: Coordinate
    width: int = 4

    @classmethod
    def from_cell(
        cls,
        cell: Cell,
        maze: mazegen.MazeGenerator,
        show_solution: bool,
    ) -> "Sprite":
        return cls(
            north=(
                Glyph.HORIZONTAL
                if cell.walls[Direction.NORTH].closed
                else Glyph.SPACE
            ),
            west=(
                Glyph.VERTICAL
                if cell.walls[Direction.WEST].closed
                else Glyph.SPACE
            ),
            south=(
                Glyph.HORIZONTAL
                if cell.walls[Direction.SOUTH].closed
                else Glyph.SPACE
            ),
            east=(
                Glyph.VERTICAL
                if cell.walls[Direction.EAST].closed
                else Glyph.SPACE
            ),
            center=cls._center(cell, maze, show_solution),
            location=cell.location,
        )

    @staticmethod
    def _center(
        cell: Cell,
        maze: mazegen.MazeGenerator,
        show_solution: bool,
    ) -> Glyph:
        if cell.location == maze.exit:
            return Glyph.EXIT

        if cell.location == maze.entry:
            return Glyph.ENTRY

        if show_solution and cell.location in maze.solution:
            return Glyph.SOLUTION

        if cell.value == reduce(lambda a, b: a | b, Direction, Direction(0)):
            return Glyph.PATTERN

        return Glyph.SPACE

    def rows(self) -> list[list[Glyph]]:
        """Return the rendered rows for this cell."""

        top = [self.north] * self.width + [Glyph.CORNER]
        middle = [self.center] * self.width + [self.east]
        bottom = [self.south] * self.width + [Glyph.CORNER]

        x, y = self.location
        if x == 0:
            top = [Glyph.CORNER] + top
            middle = [self.west] + middle
            bottom = [Glyph.CORNER] + bottom

        if y == 0:
            return [top, middle, bottom]

        return [middle, bottom]


class Ascii:
    WALL_GLYPHS = (Glyph.HORIZONTAL, Glyph.VERTICAL)

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.running = True
        self.menu_index = 0
        self.regenerate = True
        self.show_solution = False
        self.show_solution_trigger = False
        self.colorcurser = 0

    @property
    def wall_color(self) -> Colors:
        palette = list(Colors)
        return palette[self.colorcurser % len(palette)]

    def _resolve_color(self, glyph: Glyph) -> Colors | None:
        if glyph in self.WALL_GLYPHS:
            return self.wall_color
        return glyph.color

    def on_colorchange(self) -> None:
        self.colorcurser += 1

    def on_quit(self) -> None:
        self.running = False

    def on_regen(self) -> None:
        self.regenerate = True

    def on_show(self) -> None:
        self.show_solution_trigger = True

    class Option(StrEnum):
        RECREATE = "Recreate"
        SHOW = "Toggle Solution"
        CHANGE_COLOR = "Change Colorscheme"
        QUIT = "Quit"

    actions = {
        Option.CHANGE_COLOR: on_colorchange,
        Option.QUIT: on_quit,
        Option.RECREATE: on_regen,
        Option.SHOW: on_show,
    }

    def _draw_glyph(self, y: int, x: int, glyph: Glyph) -> None:
        color = self._resolve_color(glyph)
        try:
            if color is None:
                self.stdscr.addch(y, x, glyph.value[0])
            else:
                self.stdscr.addch(y, x, glyph.value[0], color.pair)
        except curses.error:
            pass

    def _draw_row(self, y: int, sprites: list[Sprite], row: int) -> None:
        x = 0

        for sprite in sprites:
            for glyph in sprite.rows()[row]:
                self._draw_glyph(y, x, glyph)
                x += 1

    def draw(self, maze: mazegen.MazeGenerator, show_solution: bool) -> None:
        self.stdscr.erase()

        sprites = [
            [Sprite.from_cell(cell, maze, show_solution) for cell in row]
            for row in maze.grid
        ]

        y = 0
        for sprite_row in sprites:
            for row in range(len(sprite_row[0].rows())):
                self._draw_row(y, sprite_row, row)
                y += 1

        y += 1

        options = list(self.Option)
        for i, option in enumerate(options):
            prefix = "> " if i == self.menu_index else "  "

            if option == self.Option.SHOW:
                suffix = ": " + ("Hidden", "Visible")[self.show_solution]
            elif option == self.Option.CHANGE_COLOR:
                suffix = ": " + self.wall_color.name
            else:
                suffix = ""

            try:
                self.stdscr.addstr(y + i, 0, prefix + option + suffix)
            except curses.error:
                pass

        self.stdscr.refresh()

    def handle_input(self, key: int) -> None:
        if key == curses.KEY_UP:
            self.menu_index -= 1
        elif key == curses.KEY_DOWN:
            self.menu_index += 1
        elif key in (10, 13, curses.KEY_ENTER):
            self.select()

        self.menu_index %= len(self.Option)

    def select(self) -> None:
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

        ascii_view = Ascii(stdscr)

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

                ascii_view.draw(maze, ascii_view.show_solution)
                ascii_view.handle_input(stdscr.getch())

                if ascii_view.regenerate:
                    break
