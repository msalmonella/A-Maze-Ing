import sys

MIN_RECURSION = 1000
ENSURE_BUFFER = 100

def calculate_recursion(width: int,
                        height: int, buffer: int) -> int:
    cells = width * height
    return max(ENSURE_BUFFER, cells + buffer)


def apply_recursion_limit(width: int, height: int, buffer: int = ENSURE_BUFFER) -> None:
    needed = calculate_recursion(width, height, buffer)
    if needed > sys.getrecursionlimit():
        sys.setrecursionlimit(needed)
