from mazegen import MazeGenerator, maze_solver
from .solver import nesw_conversion
from .generator.cell import Cell


def hex_parser(cell: Cell) -> str:
    HEX_MAP_CHARS: str = "0123456789ABCDEF"
    hex_val: int = 0
    n_val: int = 0
    e_val: int = 0
    s_val: int = 0
    w_val: int = 0
    if cell.north == True:
        n_val = 1
    if cell.east == True:
        e_val = 1
    if cell.south == True:
        s_val = 1
    if cell.west == True:
        w_val = 1
    hex_val = n_val * 1 + e_val * 2 + s_val * 4 + w_val * 8
    return HEX_MAP_CHARS[hex_val]


def write_hex_to_a_file() -> None:
    maze = MazeGenerator("config.txt")
    maze.generate_maze(0, 0, "salmonella")

    entry_x, entry_y = maze.entry
    entry_point: tuple[int, int] = entry_x, entry_y

    exit_x, exit_y = maze.exit
    exit_point: tuple[int, int] = exit_x, exit_y

    with open(maze.output_file, "w") as f:
        print(maze.output_file)
        for row in maze.maze:
            line = ""
            for cell in row:
                line += hex_parser(cell)
            f.write(line + "\n")
        f.write("\n")
        f.write(f"{entry_x},{entry_y}\n")
        f.write(f"{exit_x},{exit_y}\n")
        f.write(
            f"{"".join(nesw_conversion(maze_solver(maze, entry_point, exit_point)))}"
        )


if __name__ == "__main__":
    write_hex_to_a_file()
