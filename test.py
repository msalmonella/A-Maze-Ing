from cell import Cell
from hex_generation import seed_generator

class Pos:
    def __init__(self) -> None:
        self.x: int = 0 
        self.y: int = 0
        self.visied = False

"""Recursive function to create maze"""
def generate_maze(x: int, y: int, maze: list) -> None:
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
        if 0 <= next_x < width and 0 <= next_y < height and not maze[next_y][next_x].visited:
            generate_maze(next_x, next_y, maze)

if __name__ == "__main__":
    rng = seed_generator("salmonella")
    directions = ["N", "E", "S", "W"]
    new_move = rng.choice(directions)
    if (next == "N"):
        x = x + 1
    print(x, y)
