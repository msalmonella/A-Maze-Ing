from seeder import seed_generator
from cell import Cell, cell_generator
from maze_generation import generate_maze
from config_parser import parse_config

cfg = parse_config("config.txt")


def hex_parser(cell: Cell) -> str:
    HEX_MAP_CHARS:str = "0123456789ABCDEF"
    hex_val: int = 0
    n_val: int = 0
    e_val: int = 0
    s_val: int = 0
    w_val: int = 0
    if (cell.north == True):
        n_val = 1
    if (cell.east == True):
        e_val = 1
    if (cell.south == True):
        s_val = 1
    if (cell.west == True):
        w_val = 1
    hex_val = n_val * 1 + e_val * 2 + s_val * 4 + w_val * 8
    return (HEX_MAP_CHARS[hex_val])


if __name__ == "__main__":
    rng = seed_generator("salmonella")
    grid = cell_generator(cfg["width"], cfg["height"])
    generate_maze(0, 0, grid, rng)
    for row in grid:
        print()
        for cell in row:
            print(hex_parser(cell), end="")
