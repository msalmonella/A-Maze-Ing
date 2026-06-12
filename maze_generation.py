from cell import Cell
from hex_generation import seed_generator

class Pos:
    def __init__() -> None:
        self.x 
        self.y 
        self.visied

"""Recursive function to create maze"""
def generate_maze(x: int, y: int, grid: list) -> None:
    directions = ["N", "E", "S", "W"]
    rng.shuffle(directions)
    
    if (curr_pos == curr_pos.visited):
        generate_maze()
