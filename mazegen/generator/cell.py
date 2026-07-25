from enum import IntEnum


class Direction(IntEnum):
    """Binary counterparts of closed walls."""

    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


class Wall:
    """Represents a wall and it's closed state."""

    def __init__(self, closed: bool = True):
        self.closed = closed


class Cell:
    """Manages a collection of walls."""

    def __init__(
        self,
        north: Wall | None = None,
        east: Wall | None = None,
        south: Wall | None = None,
        west: Wall | None = None,
    ) -> None:
        self.north = north if north is not None else Wall()
        self.east = east if east is not None else Wall()
        self.south = south if south is not None else Wall()
        self.west = west if west is not None else Wall()

    @property
    def value(self) -> int:
        """Returns the integer representation of neighboring walls' states."""
        return (
            (Direction.NORTH if self.north.closed else 0)
            | (Direction.EAST if self.east.closed else 0)
            | (Direction.SOUTH if self.south.closed else 0)
            | (Direction.WEST if self.west.closed else 0)
        )
