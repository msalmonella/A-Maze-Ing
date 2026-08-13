import sys


def apply_recursion_limit(width: int, height: int) -> None:
    cell_count = width * height
    wall_count = 4
    needed = cell_count * wall_count
    if needed > sys.getrecursionlimit():
        sys.setrecursionlimit(needed)
