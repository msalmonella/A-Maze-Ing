#! /usr/bin/env python3

import sys
from sys import argv
from mazegen import MazeGenerator


def main() -> None:
    sys.setrecursionlimit(3500)

    maze = MazeGenerator(argv[1])
    maze.render()


if __name__ == "__main__":
    main()
