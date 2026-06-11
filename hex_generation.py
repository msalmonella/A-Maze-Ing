import sys
import random
import hashlib

""" Elements to pick from """
HEX_MAP_CHARS: str = "0123456789ABCDEF"

""" Random seed generator """
def seed_generator(key: str) -> random.Random:
    hash_int: int = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    rng = random.Random(hash_int)
    return rng

""" Generating grid """
def grid_gen(key: str, width: int, height: int) -> list[str]:
    rng: str = seed_generator(key)  

    return ([
        "".join(rng.choice(HEX_MAP_CHARS) for _ in range(width))
        for _ in range(height)
        ])

if __name__ == "__main__":
    grid = grid_gen(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

    for row in grid:
        print(row)
