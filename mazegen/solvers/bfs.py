import mazegen
from . import Solver
from ..models import Coordinate, Path


class BFS(Solver):
    """BFS"""

    def __call__(self, maze: mazegen.MazeGenerator) -> Path:
        path: Path = []
        node: Coordinate | None = maze.exit
        queue: Path = [maze.entry]
        visited: set[Coordinate] = {maze.entry}
        came_from: dict[Coordinate, Coordinate | None] = {maze.entry: None}
        grid = maze.grid

        def qvc_appender(
            current_pos: Coordinate, queue_pos: Coordinate
        ) -> None:
            if queue_pos not in visited:
                queue.append(queue_pos)
                visited.add(queue_pos)
                came_from[queue_pos] = current_pos

        while queue:
            current = queue.pop(0)
            x, y = current
            if current == maze.exit:
                break
            if grid[y][x].north.closed == False:
                qvc_appender(Coordinate(x, y), Coordinate(x, y - 1))
            if grid[y][x].south.closed == False:
                qvc_appender(Coordinate(x, y), Coordinate(x, y + 1))
            if grid[y][x].west.closed == False:
                qvc_appender(Coordinate(x, y), Coordinate(x - 1, y))
            if grid[y][x].east.closed == False:
                qvc_appender(Coordinate(x, y), Coordinate(x + 1, y))

        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()

        return path
