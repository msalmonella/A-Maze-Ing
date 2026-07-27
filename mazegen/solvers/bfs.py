import mazegen
from . import Solver
from ..generator.models import GridIndex


class BFS(Solver):
    """BFS"""

    def __call__(self, maze: mazegen.MazeGenerator) -> list[GridIndex]:
        path: list[GridIndex] = []
        node: GridIndex = maze.exit
        queue: list[GridIndex] = [maze.entry]
        visited: set = {maze.entry}
        came_from: dict = {maze.entry: None}
        grid = maze.grid

        def qvc_appender(current_pos: GridIndex, queue_pos: GridIndex) -> None:
            if queue_pos not in visited:
                queue.append(queue_pos)
                visited.add(queue_pos)
                came_from[queue_pos] = current_pos

        while queue:
            current = queue.pop(0)
            y, x = current
            if current == maze.exit:
                break
            if grid[y][x].north.closed == False:
                qvc_appender(GridIndex(y, x), GridIndex(y - 1, x))
            if grid[y][x].south.closed == False:
                qvc_appender(GridIndex(y, x), GridIndex(y + 1, x))
            if grid[y][x].west.closed == False:
                qvc_appender(GridIndex(y, x), GridIndex(y, x - 1))
            if grid[y][x].east.closed == False:
                qvc_appender(GridIndex(y, x), GridIndex(y, x + 1))

        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()

        return path
