"""Maze grid, cell and wall representations."""

from .models import Direction, Coordinate
from .errors import LockedWallError


class Wall:
    """Represents a wall and it's closed state.

    Args:
        closed (bool): Whether the wall is open or close.
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
    """Manages a collection of walls.

    Attributes:
        location (Coordinate):
            The cell's position inside a grid.
        walls (dict[Direction, Wall]):
            A mapping of directions to their corresponding walls.
    """

    def __init__(
        self,
        location: Coordinate,
        north: Wall | None = None,
        east: Wall | None = None,
        south: Wall | None = None,
        west: Wall | None = None,
    ) -> None:
        """Initialize a cell and its walls.

        Args:
            location: The cell's coordinate.
            north: The wall to the north, or a default wall.
            east: The wall to the east, or a default wall.
            south: The wall to the south, or a default wall.
            west: The wall to the west, or a default wall.
        """

        self.location = location
        self.walls = {
            Direction.NORTH: north if north is not None else Wall(),
            Direction.EAST: east if east is not None else Wall(),
            Direction.SOUTH: south if south is not None else Wall(),
            Direction.WEST: west if west is not None else Wall(),
        }

    @property
    def value(self) -> Direction:
        """Get the bitwise flag representation of neighboring walls."""

        value = Direction(0)
        for direction, wall in self.walls.items():
            if wall.closed:
                value |= direction
        return value

    def lock(self) -> None:
        """Locks all of the walls without raising an error.

        Unlocked walls are closed before being locked. Already locked walls
        are left unchanged.
        """

        for wall in self.walls.values():
            if not wall.locked:
                wall.closed = True
                wall.locked = True

    def neighbor(self, direction: Direction) -> Coordinate:
        """Returns the coordinate of a neighboring cell in a given direction

        Args:
            direction: The direction of the neighboring cell.

        Returns:
            Coordinate:
                The coordinate adjacent to this cell in the given direction.
        """

        offset = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }
        dx, dy = offset[direction]
        x, y = self.location

        return Coordinate(x + dx, y + dy)


Grid = list[list[Cell]]
