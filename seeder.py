import random
import hashlib

""" Random seed generator """
def seed_generator(key: str) -> random.Random:
    hash_int: int = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    rng = random.Random(hash_int)
    return rng
