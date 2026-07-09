#! /usr/bin/env python3

from maze import (
    parse_config,
    cell_generator,
    seed_generator,
    generate_maze,
    maze_solver,
)
from maze.solver import nesw_conversion

# import mlx

cfg = parse_config("config.txt")

rng = seed_generator("salmonella")
grid = cell_generator(cfg["width"], cfg["height"])
generate_maze(0, 0, grid, rng)

if __name__ == "__main__":

    # print(maze_solver(grid, cfg["entry"], cfg["exit"]))

    entry_point = cfg["entry"]
    exit_point = cfg["exit"]

    path = maze_solver(grid, entry_point, exit_point)
    converted: list[str] = nesw_conversion(path)
    print("".join(converted))
