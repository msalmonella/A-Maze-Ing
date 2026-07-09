from . import parse_config

cfg = parse_config("config.txt")


def mazer_the_miner(
    maze: list, next_pos: tuple, prev_pos: tuple, direction: str
) -> None:
    """Digging into walls"""
    next_x, next_y = next_pos
    x, y = prev_pos
    if direction == "N":
        maze[y][x].north = False
        maze[next_y][next_x].south = False
    elif direction == "S":
        maze[y][x].south = False
        maze[next_y][next_x].north = False
    elif direction == "E":
        maze[y][x].east = False
        maze[next_y][next_x].west = False
    elif direction == "W":
        maze[y][x].west = False
        maze[next_y][next_x].east = False


def generate_maze(x: int, y: int, maze: list, rng) -> None:
    """Recursive function to create maze"""
    maze[y][x].visited = True
    directions = ["N", "E", "S", "W"]
    rng.shuffle(directions)
    for choice in directions:
        next_x, next_y = x, y
        if choice == "N":
            next_x, next_y = x, y - 1
        elif choice == "S":
            next_x, next_y = x, y + 1
        elif choice == "E":
            next_x, next_y = x + 1, y
        elif choice == "W":
            next_x, next_y = x - 1, y
        if (
            0 <= next_x < cfg["width"]
            and 0 <= next_y < cfg["height"]
            and not maze[next_y][next_x].visited
        ):
            mazer_the_miner(maze, (next_x, next_y), (x, y), choice)
            generate_maze(next_x, next_y, maze, rng)
