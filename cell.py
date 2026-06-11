class Cell:
    def __init__(self, north: bool = True, east: bool = True, south: bool = True, west: bool = True) -> None:
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.visited: bool = False

def cell_generator(width: int, height: int) -> list[Cell]:
    grid = []
    for _ in range(width):
        row = []
        for _ in range(height):
            row.append(Cell()) 
        grid.append(row)
    return grid
