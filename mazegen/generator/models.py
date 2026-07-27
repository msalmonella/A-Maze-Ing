from typing import NamedTuple
from enum import IntEnum


class Direction(IntEnum):
    """Binary representation of closed walls."""

    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


class GridIndex(NamedTuple):
    """Indicates a position on a maze grid."""

    row: int
    column: int


Path = list[GridIndex]
