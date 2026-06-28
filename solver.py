from config_parser import parse_config
from seeder import seed_generator
from cell import cell_generator
from maze_generation import generate_maze

cfg = parse_config("config.txt")
queue: list[tuple] = []
visited: set = set() 
came_from: dict = {}

rng = seed_generator("salmonella")
grid = cell_generator(cfg["width"], cfg["height"])
generate_maze(0, 0, grid, rng)


def qvc_appender(current_pos, queue_pos: tuple) -> None:
    queue.append(queue_pos)
    visited.add(current_pos)


def maze_solver(maze, entry_point, exit_point) -> None:
    x, y = entry_point
    if maze[y][x].north == False:
        qvc_appender((x, y), (x, y - 1))
    if maze[y][x].south == False:
        qvc_appender((x, y), (x, y + 1))
    if maze[y][x].west == False:
        qvc_appender((x, y), (x - 1, y))
    if maze[y][x].east == False:
        qvc_appender((x, y), (x + 1, y))
