#! /usr/bin/env python3

import sys
from mazegen import MazeGenerator, MazeError


def main() -> None:
    if not len(sys.argv) == 2:
        print(f"Usage: {sys.argv[0]} <config_file>")
        sys.exit(1)

    try:
        maze = MazeGenerator(sys.argv[1])
        maze.render()
    except MazeError as e:
        print("Maze Error:", e.args[0], file=sys.stderr)
        for arg in e.args[1:]:
            print(" ", arg, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("Unexpected error:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
