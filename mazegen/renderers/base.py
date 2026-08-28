import curses
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Self
import mazegen


class Colors(IntEnum):
    def __new__(cls, pair_id: int, fg: int, bg: int = -1) -> Self:
        obj = int.__new__(cls, pair_id)
        obj._value_ = pair_id
        return obj

    def __init__(self, pair_id: int, fg: int, bg: int = -1):
        self.fg = fg
        self.bg = bg

    WHITE = (1, curses.COLOR_WHITE)
    RED = (2, curses.COLOR_RED)
    GREEN = (3, curses.COLOR_GREEN)
    BLUE = (4, curses.COLOR_BLUE)
    YELLOW = (5, curses.COLOR_YELLOW)
    CYAN = (6, curses.COLOR_CYAN)
    MAGENTA = (7, curses.COLOR_MAGENTA)

    @classmethod
    def init_pairs(cls) -> None:
        curses.start_color()
        curses.use_default_colors()
        for member in cls:
            curses.init_pair(member.value, member.fg, member.bg)

    @property
    def pair(self) -> int:
        return curses.color_pair(self.value)


class Renderer(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator) -> None:
        pass
