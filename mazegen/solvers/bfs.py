from . import Solver
from ..models import Coordinate, Path, Direction
from ..cell import Grid
from ..models import Mandatory


class BFS(Solver):
    """BFS"""

    def __call__(self, grid: Grid, config: Mandatory) -> Path:
        path: Path = []
        node: Coordinate | None = config.exit
        queue: Path = [config.entry]
        visited: set[Coordinate] = {config.entry}
        came_from: dict[Coordinate, Coordinate | None] = {config.entry: None}

        def qvc_appender(
            current_pos: Coordinate, queue_pos: Coordinate
        ) -> None:
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
