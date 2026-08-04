from .models import Direction
from .errors import LockedWallError


class Wall:
    """Represents a wall and it's closed state.

    Args:
        closed (bool): Represents open/close state of the wall.
        locked (bool): Whether it is restricted to open/close the wall.
    """

    def __init__(self, closed: bool = True, locked: bool = True):
        self._closed = closed
        self.locked = locked

    @property
    def closed(self) -> bool:
        """Representation of the wall's closed state.

        Raises:
            LockedWallError: Changing the `closed` state of a locked wall.
        """
        return self._closed

    @closed.setter
    def closed(self, value: bool) -> None:
        if self.locked:
            raise LockedWallError(
                "Cannot change 'closed' state of a locked wall"
            )
        self._closed = value


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

    def lock(self) -> None:
        """Locks all of the walls without raising an error."""
        for wall in [self.north, self.east, self.south, self.west]:
            if not wall.locked:
                wall.closed = True
                wall.locked = True
