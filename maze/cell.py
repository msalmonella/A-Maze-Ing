class Cell:
    def __init__(
        self,
        north: bool = True,
        east: bool = True,
        south: bool = True,
        west: bool = True,
    ) -> None:
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.visited: bool = False

    def __repr__(self) -> str:
        return f"N:{int(self.north)} E:{int(self.east)} S:{int(self.south)} W:{int(self.west)}"


def cell_generator(width: int, height: int) -> list[list[Cell]]:
    """Inserting closed walls to entire map"""
    grid = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append(Cell())
        grid.append(row)
    return grid
