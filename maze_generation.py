from config_parser import parse_config
from cell import Cell, cell_generator
from hex_generation import seed_generator

cfg = parse_config("config.txt")

class Pos:
    def __init__(self) -> None:
        self.x: int = 0 
        self.y: int = 0
        self.visied = False

"""Recursive function to create maze"""
def generate_maze(x: int, y: int, maze: list) -> None:
    maze[y][x].visited = True
    directions = ["N", "E", "S", "W"]
    rng.shuffle(directions)
    for choice in directions:
        if choice == "N":
            next_x, next_y = x, y - 1
        elif choice == "S":
            next_x, next_y = x, y + 1
        elif choice == "E":
            next_x, next_y = x + 1, y
        elif choice == "W":
            next_x, next_y = x - 1, y
        if 0 <= next_x < cfg["width"] and 0 <= next_y < cfg["height"] and not maze[next_y][next_x].visited:
            generate_maze(next_x, next_y, maze)

if __name__ == "__main__":
    rng = seed_generator("salmonella")
    grid = cell_generator(cfg["width"], cfg["height"])
    generate_maze(0, 0, grid)
    for row in grid:
        print(row)
