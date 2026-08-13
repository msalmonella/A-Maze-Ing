#! /usr/bin/env python3

from sys import argv
from mazegen import MazeGenerator


def main() -> None:
    maze = MazeGenerator(argv[1])
    maze.render()


if __name__ == "__main__":
    main()
