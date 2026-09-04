"""Breadth-first search solver for grid-based pathfinding."""

from . import Solver
from ..models import Coordinate, Path, Direction
from ..cell import Grid
from ..models import Mandatory


class BFS(Solver):
    """Solve grid paths using the breadth-first search algorithm."""

    def __call__(self, grid: Grid, config: Mandatory) -> Path:
        """Find the shortest path from the entry to the exit.

        Args:
            grid (Grid): The grid to search for a path through.
            config (Mandatory):
                Configuration containing the entry and exit coordinates.

        Returns:
            Path: A path from the entry coordinate to the exit coordinate.
        """

        path: Path = []
        node: Coordinate | None = config.exit
        queue: Path = [config.entry]
        visited: set[Coordinate] = {config.entry}
        came_from: dict[Coordinate, Coordinate | None] = {config.entry: None}

        def qvc_appender(
            current_pos: Coordinate, queue_pos: Coordinate
        ) -> None:
            """Add an unvisited neighboring coordinate to the search queue."""

            if queue_pos not in visited:
                queue.append(queue_pos)
                visited.add(queue_pos)
                came_from[queue_pos] = current_pos

        while queue:
            current = queue.pop(0)
            if current == config.exit:
                break

            x, y = current
            cell = grid[y][x]

            for direction in Direction:
                if not cell.walls[direction].closed:
                    qvc_appender(current, cell.neighbor(direction))

        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()

        return path
