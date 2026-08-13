from typing import NamedTuple
from enum import IntFlag


class Direction(IntFlag):
    """Binary representation of closed walls."""

    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


class Coordinate(NamedTuple):
    """Indicates a position on a maze grid."""

    x: int
    y: int


Path = list[Coordinate]
