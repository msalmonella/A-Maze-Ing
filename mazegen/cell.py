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
        self.walls = {
            Direction.NORTH: north if north is not None else Wall(),
            Direction.EAST: east if east is not None else Wall(),
            Direction.SOUTH: south if south is not None else Wall(),
            Direction.WEST: west if west is not None else Wall(),
        }

    @property
    def value(self) -> int:
        """Returns the integer representation of neighboring walls' states."""

        return sum(
            direction for direction, wall in self.walls.items() if wall.closed
        )

    def lock(self) -> None:
        """Locks all of the walls without raising an error."""

        for wall in self.walls.values():
            if not wall.locked:
                wall.closed = True
                wall.locked = True
