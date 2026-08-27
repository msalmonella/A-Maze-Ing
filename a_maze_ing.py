#! /usr/bin/env python3

from sys import argv
from mazegen import MazeGenerator, MazeError


def main() -> None:
    try:
        maze = MazeGenerator(argv[1])
        maze.render()
    except MazeError as e:
        print(e.args[0])
        for arg in e.args[1:]:
            print(" ", arg)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()
