from .config_parser import parse_config
from .cell import Cell, cell_generator
from .seeder import seed_generator


class MazeGenerator:
    maze: list[list[Cell]]

    def __init__(self, config_path: str):
        cfg = parse_config(config_path)

        self.width = cfg["width"]
        self.height = cfg["height"]
        self.entry = cfg["entry"]
        self.exit = cfg["exit"]
        self.output_file = cfg["output_file"]
        self.perfect = cfg["perfect"]

        self.maze = cell_generator(self.width, self.height)

    def _mazer_the_miner(
        self, next_pos: tuple, prev_pos: tuple, direction: str
    ) -> None:
        """Digging into walls"""
        next_x, next_y = next_pos
        x, y = prev_pos
        if direction == "N":
            self.maze[y][x].north = False
            self.maze[next_y][next_x].south = False
        elif direction == "S":
            self.maze[y][x].south = False
            self.maze[next_y][next_x].north = False
        elif direction == "E":
            self.maze[y][x].east = False
            self.maze[next_y][next_x].west = False
        elif direction == "W":
            self.maze[y][x].west = False
            self.maze[next_y][next_x].east = False

    def generate_maze(self, x: int, y: int, seed: str = "") -> None:
        """Recursive function to create maze"""
        self.maze[y][x].visited = True
        directions = ["N", "E", "S", "W"]
        rng = seed_generator(seed)
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
                0 <= next_x < self.width
                and 0 <= next_y < self.height
                and not self.maze[next_y][next_x].visited
            ):
                self._mazer_the_miner((next_x, next_y), (x, y), choice)
                self.generate_maze(next_x, next_y, seed)
