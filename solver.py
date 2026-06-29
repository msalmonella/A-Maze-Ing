from config_parser import parse_config
from seeder import seed_generator
from cell import cell_generator
from maze_generation import generate_maze

cfg = parse_config("config.txt")

rng = seed_generator("salmonella")
grid = cell_generator(cfg["width"], cfg["height"])
generate_maze(0, 0, grid, rng)



""" BFS """
def maze_solver(maze, entry_point, exit_point) -> list[tuple[int, int]]:
    path: list = []
    node = exit_point
    queue: list[tuple] = [entry_point]
    visited: set = {entry_point}
    came_from: dict = {entry_point: None}

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


if __name__ == "__main__":
    
    print(maze_solver(grid, cfg["entry"], cfg["exit"]))
