"""Render mazes interactively using a curses-based ASCII interface."""

import curses
import time
from enum import Enum, StrEnum
from functools import reduce
from dataclasses import dataclass
import mazegen
from . import Renderer, Colors
from ..cell import Cell
from ..models import Direction, Coordinate, Path
from ..models import Mandatory


class Glyph(Enum):
    """Character representations of a Cell's features."""

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
        """Return the default color associated with the glyph.

        Returns:
            Colors:
                The color assigned to the glyph, or `None` if the glyph has no
                default color.
        """

        return {
            Glyph.HORIZONTAL: Colors.WHITE,
            Glyph.VERTICAL: Colors.WHITE,
            Glyph.EXIT: Colors.RED,
            Glyph.ENTRY: Colors.GREEN,
            Glyph.SOLUTION: Colors.YELLOW,
        }.get(self)


@dataclass(frozen=True)
class Sprite:
    """Represent the visual elements of a single maze cell.

    A sprite contains the glyphs used to render the four walls, the
    cell center, and the cell's location within the maze.
    """

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
        config: Mandatory,
        solution: Path,
        show_solution: bool,
    ) -> "Sprite":
        """Create a sprite from a maze cell.

        Args:
            cell (Cell): The maze cell to render.
            config (Mandatory):
                Maze configuration containing the entry and exit coordinates.
            solution (Path): The solution path through the maze.
            show_solution (bool):
                Whether solution cells and walls should be rendered.

        Returns:
            Sprite: A sprite representing the visual state of the cell.
        """

        return cls(
            north=cls._walls(cell, solution, show_solution, Direction.NORTH),
            west=cls._walls(cell, solution, show_solution, Direction.WEST),
            south=cls._walls(cell, solution, show_solution, Direction.SOUTH),
            east=cls._walls(cell, solution, show_solution, Direction.EAST),
            center=cls._center(cell, config, solution, show_solution),
            location=cell.location,
        )

    @staticmethod
    def _walls(
        cell: Cell,
        solution: Path,
        show_solution: bool,
        direction: Direction,
    ) -> Glyph:
        """Determine the glyph used to render a cell wall.

        Open walls that form part of the solution are rendered using the
        solution glyph when the solution is visible.

        Args:
            cell (Cell): The maze cell whose wall is being rendered.
            solution (Path): The solution path through the maze.
            show_solution (bool): Whether the solution should be displayed.
            direction (Direction): The direction of the wall to render.

        Returns:
            Glyph: The glyph representing the wall.
        """

        glyphs = {
            Direction.NORTH: Glyph.HORIZONTAL,
            Direction.WEST: Glyph.VERTICAL,
            Direction.SOUTH: Glyph.HORIZONTAL,
            Direction.EAST: Glyph.VERTICAL,
        }

        if cell.walls[direction].closed:
            return glyphs[direction]

        if (
            show_solution
            and cell.location in solution
            and cell.neighbor(direction) in solution
        ):
            return Glyph.SOLUTION
        return Glyph.SPACE

    @staticmethod
    def _center(
        cell: Cell,
        config: Mandatory,
        solution: Path,
        show_solution: bool,
    ) -> Glyph:
        """Determine the glyph used to render the center of a cell.

        Entry and exit cells take precedence over the solution and pattern
        indicators.

        Args:
            cell (Cell): The maze cell whose center is being rendered.
            config (Mandatory):
                Maze configuration containing the entry and exit coordinates.
            solution (Path): The solution path through the maze.
            show_solution (bool): Whether the solution should be displayed.

        Returns:
            Glyph: The glyph representing the center of the cell.
        """

        if cell.location == config.exit:
            return Glyph.EXIT

        if cell.location == config.entry:
            return Glyph.ENTRY

        if show_solution and cell.location in solution:
            return Glyph.SOLUTION

        if cell.value == reduce(lambda a, b: a | b, Direction, Direction(0)):
            return Glyph.PATTERN

        return Glyph.SPACE

    def rows(self) -> list[list[Glyph]]:
        """Return the rows of glyphs used to render the sprite.

        Returns:
            A list containing the top, middle, and bottom rows of the sprite.
            The top row is omitted for cells that are not on the first maze
            row.
        """

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
    """Manage the interactive curses-based ASCII maze display."""

    WALL_GLYPHS = (Glyph.HORIZONTAL, Glyph.VERTICAL)

    def __init__(self, stdscr: curses.window):
        """Initialize the ASCII maze view.

        Args:
            stdscr (curses.window):
                The curses window on which the maze is rendered.
        """
        self.stdscr = stdscr
        self.running = True
        self.menu_index = 0
        self.regenerate = True
        self.show_solution = False
        self.color_cursor = 0

    @property
    def wall_color(self) -> Colors:
        """Return the currently selected wall color.

        Returns:
            Colors: The color currently selected for maze walls.
        """

        palette = list(Colors)
        return palette[self.color_cursor % len(palette)]

    def _resolve_color(self, glyph: Glyph) -> Colors | None:
        """Resolve the display color for a glyph.

        Wall glyphs use the currently selected wall color, while other glyphs
        use their predefined colors.

        Args:
            glyph (Glyph): The glyph whose color should be determined.

        Returns:
            Colors: The color to use when rendering the glyph, or `None` if it
            should be rendered without color.
        """

        if glyph in self.WALL_GLYPHS:
            return self.wall_color
        return glyph.color

    def on_color_change(self) -> None:
        """Advance to the next available wall color."""
        self.color_cursor += 1

    def on_quit(self) -> None:
        """Stop the interactive maze display."""
        self.running = False

    def on_regen(self) -> None:
        """Request that the maze be regenerated."""
        self.regenerate = True

    def on_show(self) -> None:
        """Toggle visibility of the maze solution."""
        self.show_solution = not self.show_solution

    class Option(StrEnum):
        """Available actions in the interactive menu."""

        RECREATE = "Recreate"
        SHOW = "Toggle Solution"
        CHANGE_COLOR = "Change Wall Color"
        QUIT = "Quit"

    actions = {
        Option.CHANGE_COLOR: on_color_change,
        Option.QUIT: on_quit,
        Option.RECREATE: on_regen,
        Option.SHOW: on_show,
    }

    def _draw_info(self, maze: mazegen.MazeGenerator) -> int:
        """Draw maze configuration information.

        Args:
            maze (mazegen.MazeGenerator):
                The maze generator whose configuration and state should be
                displayed.

        Returns:
            int: The number of terminal rows consumed by the information panel.
        """

        config = maze.config
        info = [
            "Maze Configuration",
            "",
            f"{'Size:':16}"
            f"{config.width} x {config.height}"
            f" ({config.width * config.height} cells)",
            f"{'Entry:':16}" f"{config.entry}",
            f"{'Exit:':16}" f"{config.exit}",
            f"{'Output File:':16}" f"{config.output_file}",
            f"{'Perfect:':16}" f"{config.perfect}",
            "",
            f"{'Seed:':16}"
            + (f"'{maze.seed}'" if maze.seed else "Not provided"),
            f"{'Speed:':16}"
            + (f"{maze.sps} steps/sec" if maze.sps != 0 else "Instant"),
            f"{'Solution:':16}"
            + (
                f"{len(maze.solution)} cells"
                if maze.solution
                else "Generating"
            ),
            "",
        ]

        if not maze.pattern_can_fit():
            info.extend(["WARNING: 42 pattern does not fit. Ommitting.", ""])

        row_count = 0
        for line in info:
            try:
                self.stdscr.addstr(row_count, 0, line)
                row_count += 1
            except curses.error:
                pass

        return row_count

    def _draw_glyph(self, y: int, x: int, glyph: Glyph) -> None:
        """Draw a single glyph at a terminal position.

        Args:
            y (int): The row at which to draw the glyph.
            x (int): The column at which to draw the glyph.
            glyph (Glyph): The glyph to draw.
        """

        color = self._resolve_color(glyph)

        try:
            if color is None:
                self.stdscr.addch(y, x, glyph.value[0])
            else:
                self.stdscr.addch(y, x, glyph.value[0], color.pair)
        except curses.error:
            pass

    def _draw_row(self, y: int, sprites: list[Sprite], row: int) -> None:
        """Draw one rendered row of maze sprites.

        Args:
            y (int): The terminal row at which to draw.
            sprites (list[Sprites]): The sprites making up the maze row.
            row (int): The sprite row index to render.
        """

        x = 0

        for sprite in sprites:
            for glyph in sprite.rows()[row]:
                self._draw_glyph(y, x, glyph)
                x += 1

    def draw(self, maze: mazegen.MazeGenerator, show_solution: bool) -> None:
        """Render the maze, information panel, and menu.

        Args:
            maze (mazegen.MazeGenerator):
                The maze generator containing the maze to render.
            show_solution (bool): Whether the maze solution should be visible.
        """

        self.stdscr.erase()

        sprites = [
            [
                Sprite.from_cell(
                    cell, maze.config, maze.solution, show_solution
                )
                for cell in row
            ]
            for row in maze.grid
        ]

        row_count = 0

        row_count += self._draw_info(maze)

        for sprite_row in sprites:
            for row in range(len(sprite_row[0].rows())):
                self._draw_row(row_count, sprite_row, row)
                row_count += 1

        row_count += 1

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
                self.stdscr.addstr(row_count + i, 0, prefix + option + suffix)
            except curses.error:
                pass

        self.stdscr.refresh()

    def handle_input(self, key: int) -> None:
        """Handle a keyboard input event.

        Args:
            key (int): The curses key code received from the terminal.
        """

        if key == curses.KEY_UP:
            self.menu_index -= 1
        elif key == curses.KEY_DOWN:
            self.menu_index += 1
        elif key in (10, 13, curses.KEY_ENTER):
            self.select()

        self.menu_index %= len(self.Option)

    def select(self) -> None:
        """Execute the action associated with the selected menu option."""

        options = list(self.Option)
        option = options[self.menu_index]
        action = self.actions[option]
        action(self)


class AsciiRenderer(Renderer):
    """Renderer of a maze that uses a curses-based ASCII representation"""

    def __call__(self, maze: mazegen.MazeGenerator) -> None:
        """Render a maze using the curses-based ASCII renderer.

        Args:
            maze (mazegen.MazeGenerator):
                The maze generator containing the maze to render.
        """
        curses.wrapper(self.main, maze)

    def main(self, stdscr: curses.window, maze: mazegen.MazeGenerator) -> None:
        """Run the interactive curses rendering loop.

        Args:
            stdscr (curses.window):
                The curses window used for rendering and input.
            maze (mazegen.MazeGenerator):
                The maze generator used to create and display the maze.
        """

        Colors.init_pairs()
        curses.curs_set(0)
        # stdscr.keypad(True)
        stdscr.timeout(0)

        ascii_view = Ascii(stdscr)

        while ascii_view.regenerate:
            ascii_view.regenerate = False
            generation = maze.generate()
            generating = True

            stdscr.clear()

            try:
                next(generation)
            except StopIteration:
                generating = False

            step_delay = 1 / maze.sps if maze.sps else 0
            last_step = time.monotonic()

            while ascii_view.running:
                ascii_view.handle_input(stdscr.getch())

                if ascii_view.regenerate:
                    try:
                        while True:
                            next(generation)
                    except StopIteration:
                        break

                now = time.monotonic()

                if generating and now - last_step >= step_delay:
                    try:
                        if step_delay == 0:
                            while True:
                                next(generation)
                        else:
                            next(generation)
                        last_step = now
                    except StopIteration:
                        generating = False

                ascii_view.draw(maze, ascii_view.show_solution)
