from config_parser import parse_config
from seeder import seed_generator
from cell import cell_generator
from maze_generation import generate_maze

cfg = parse_config("config.txt")

rng = seed_generator("salmonella")
grid = cell_generator(cfg["width"], cfg["height"])
generate_maze(0, 0, grid, rng)


def maze_solver(maze, entry_point, exit_point) -> None:
    x, y = entry_point
    if maze[y][x].north == False:
        # do


# i have to check if the path is possible if yes
# will be remembering where i come from next time
