#! /usr/bin/env python3

from sys import argv
from mazegen import MazeGenerator
from mazegen.solvers import BFS
from mazegen.renders import HexWriter


def main() -> None:
    maze = MazeGenerator(argv[1])
    maze.generate_maze(seed="salmonella")
    write_hex_to_a_file(maze)


if __name__ == "__main__":
    main()
