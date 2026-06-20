from seeder import seed_generator
from cell import cell_generator
from maze_generation import generate_maze
from config_parser import parse_config

cfg = parse_config("config.txt")

if __name__ == "__main__":
    rng = seed_generator("salmonella")
    grid = cell_generator(cfg["width"], cfg["height"])
    generate_maze(0, 0, grid, rng)
    for row in grid:
        print(row)
