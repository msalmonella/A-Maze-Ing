#! /usr/bin/env python3

from sys import argv
from mazegen import MazeGenerator, maze_solver
from mazegen.solver import nesw_conversion


def main() -> None:
    maze = MazeGenerator(argv[1])
    maze.generate_maze(0, 0)

    entry_point = maze.entry
    exit_point = maze.exit

    path = maze_solver(maze, entry_point, exit_point)
    converted: list[str] = nesw_conversion(path)
    print("".join(converted))


if __name__ == "__main__":
    main()
