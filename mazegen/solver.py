from .generator import MazeGenerator


def maze_solver(
    maze_gen: MazeGenerator, entry_point, exit_point
) -> list[tuple[int, int]]:
    """BFS"""
    path: list = []
    node = exit_point
    queue: list[tuple] = [entry_point]
    visited: set = {entry_point}
    came_from: dict = {entry_point: None}
    maze = maze_gen.maze

    def qvc_appender(current_pos, queue_pos: tuple) -> None:
        if queue_pos not in visited:
            queue.append(queue_pos)
            visited.add(queue_pos)
            came_from[queue_pos] = current_pos

    while queue:
        current = queue.pop(0)
        x, y = current
        if current == exit_point:
            break
        if maze[y][x].north == False:
            qvc_appender((x, y), (x, y - 1))
        if maze[y][x].south == False:
            qvc_appender((x, y), (x, y + 1))
        if maze[y][x].west == False:
            qvc_appender((x, y), (x - 1, y))
        if maze[y][x].east == False:
            qvc_appender((x, y), (x + 1, y))

    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()

    return path


def nesw_conversion(path: list[tuple[int, int]]) -> list[str]:
    nesw: list[str] = []
    for i in range(len(path) - 1):
        current = path[i]
        next_cell = path[i + 1]

        current_x, current_y = current
        next_x, next_y = next_cell

        if next_y > current_y:
            nesw.append("N")

        if next_x > current_x:
            nesw.append("E")

        if current_y > next_y:
            nesw.append("S")

        if current_x > next_x:
            nesw.append("W")

    return nesw
