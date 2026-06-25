from seeder import seed_generator
from cell import Cell, cell_generator
from maze_generation import generate_maze
from config_parser import parse_config
from solver import maze_solver

cfg = parse_config("config.txt")

entry_x, entry_y = cfg["entry"]
entry_point: tuple[int, int] = entry_x, entry_y

exit_x, exit_y = cfg["exit"]
exit_point: tuple[int, int] = exit_x, exit_y


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


def write_hex_to_a_file() -> None:
    rng = seed_generator("salmonella")
    grid = cell_generator(cfg["width"], cfg["height"])
    generate_maze(0, 0, grid, rng)
    with open(cfg["output_file"], "w") as f:
        for row in grid:
            line = ""
            for cell in row:
                line += hex_parser(cell)
            f.write(line + "\n")
        f.write("\n")
        f.write(f"{cfg["entry"][0]},{cfg["entry"][1]}\n")
        f.write(f"{cfg["exit"][0]},{cfg["exit"][1]}\n")
        f.write(f"{maze_solver(grid, entry_point, exit_point)}")
        

if __name__ == "__main__":
    write_hex_to_a_file()
