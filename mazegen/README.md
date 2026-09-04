_This project has been created as part of the 42 curriculum by cbozkurt, adede._

# mazegen-hermanos

**mazegen-hermanos** contains the maze generator implementation for the project **A-Maze-ing**.

## Description

A-Maze-ing is a Python project that generates and displays mazes based on a user-provided configuration file.

This package contains a reusable `MazeGenerator` class packaged separately so that the maze generation logic can be reused in future Python projects.

This package has two main generation modes:

- **Perfect maze:** a maze with exactly one path between any two cells, including the entrance and exit.
- **Non-perfect maze:** a playable maze designed for a Pac-Man-like game, with multiple independent routes, connected corridors, open corners and centre, and few dead ends.

The generated maze is:

1.  Configured through a text file.
2.  Generated using a randomized maze generation algorithm.
3.  Solved a path from the entrance to the exit.
4.  Saved using the required hexadecimal wall representation.
5.  Visually displayed in the terminal or through a graphical interface.

# Instructions

# Configuration File

The program expects a configuration file containing one `KEY=VALUE` pair per line.

Lines beginning with `#` are treated as comments and ignored.

## Configuration Parameters

| Key           | Required | Description                           | Example                  |
| ------------- | -------- | ------------------------------------- | ------------------------ |
| `WIDTH`       | Yes      | Number of cells horizontally          | `WIDTH=20`               |
| `HEIGHT`      | Yes      | Number of cells vertically            | `HEIGHT=15`              |
| `ENTRY`       | Yes      | Entry cell coordinates `(x,y)`        | `ENTRY=0,0`              |
| `EXIT`        | Yes      | Exit cell coordinates `(x,y)`         | `EXIT=19,14`             |
| `OUTPUT_FILE` | Yes      | Path/name of generated maze file      | `OUTPUT_FILE=maze.txt`   |
| `PERFECT`     | Yes      | Enables perfect maze mode             | `PERFECT=True`           |
| `SEED`        | No       | Seed used for reproducible generation | `SEED=42`                |
| `SPS`         | No       | Generation steps per second (roughly) | `SPS=60`                 |
| `ALGORITHM`   | No       | Maze generation algorithm             | `ALGORITHM=Prim`         |
| `SOLVER`      | No       | Visualisation mode                    | `SOLVER=BFS`             |
| `RENDERER`    | No       | Renderer that manages the display     | `RENDERER=AsciiRenderer` |

### Valid Values

- `WIDTH` and `HEIGHT` must be a positive integer greater that 0.

- Both `ENTRY` and `EXIT` must be inside the maze and not be the same with each other. They can't pe placed on top of the 42 pattern also.

- For `PERFECT`, when it is `True`, the generated maze contains exactly one path between the entry and exit; when it is `False`, the maze is generated as a playable board with multiple routes.

- `SPS` must be a positive integer or 0. The built-in renderer should display the generation instantaneously instead of step-by-step if `SPS` is specified as 0.

- The 'operations' (`ALGORITHM`, `SOLVER` and `RENDERER`) can only reference built-in methods. To customize the operations further, modify the `operations` attribute of the `MazeGenerator` class.

  Available algorithms for `ALGORITHM`:
  - `MazerTheMiner`
  - `Prim`

  Available solvers for `SOLVER`:
  - `BFS`

  Available solvers for `SOLVER`:
  - `AsciiRenderer`

# Maze Generation Algorithm

## Chosen Algorithm

This package uses **Depth-First Search (DFS)** and **Prim's Algorithm**.

### How It Works

For **DFS** (Recursive Backtracker):

1.  Start from a randomly selected cell.
2.  Mark the cell as visited.
3.  Select an unvisited neighbouring cell.
4.  Remove the wall between the current cell and the selected neighbour.
5.  Continue recursively from the new cell.
6.  If there are no unvisited neighbours, backtrack to the previous cell.
7.  Continue until every cell has been visited.

Mazes generated with a _depth-first search (DFS)_ have a low branching factor and contain many long corridors, because the algorithm explores as far as possible along each branch before backtracking.

Instead, with **Prim's**:

1.  Start from a randomly selected cell.
2.  Add the cell to the 'frontiers'.
3.  While there are frontiers:
    1.  Select a random frontier. Skip if visited.
    2.  Connect the current frontier to the maze by opening the related wall.
    3.  Add all the potential neighbouring cells to the frontiers.
    4.  Move the current frontier to visited

This algorithm tends to produce regular patterns which are fairly easy to solve, because the effect of this algorithm is to produce a _minimal spanning tree_ from a graph with equally weighted edges.

Both methods produce a spanning-tree structure, which naturally provide a perfect maze with a unique path between cells.

### Why We Chose This Algorithm

We chose **DFS** because:

1. It is relatively simple to implement.
2. It provides interesting winding corridors.

We chose **Prim's** because:

1. It is fairly uniform.
2. It provides a better playground.

### Non-Perfect Maze Generation

When `PERFECT=False`, the initial maze is modified/generated to support gameplay requirements.

The resulting maze must:

- Remain fully connected.
- Have open corridors in the four corners.
- Have an open centre.
- Contain multiple independent routes.
- Avoid large open areas.
- Have few dead ends.
- Remain suitable for a Pac-Man-like game.

On a PERFECT maze, scan all the cells one-by-one and detect the dead-ends. When detected, open a wall starting with the wall in the middle. This ensures no area with a width more than 2 is formed (like a 3x3 area).

# Maze Representation

Internally, each cell stores four `Wall` instances:

            North
              |
         +----+----+
         |         |
    West |  Cell   | East
         |         |
         +----+----+
              |
            South

Represented as flags of such:

| Direction | Binary representation |
| --------- | --------------------- |
| NORTH     | 0001                  |
| EAST      | 0010                  |
| SOUTH     | 0100                  |
| WEST      | 1000                  |

A closed wall has bit value `1` and an open wall has bit value `0`.

For example:

    3 = 0011

means North and East are closed.

    A = 1010

means East and West are closed.

Neighbouring cells always have coherent shared walls. For example, if a cell has an open East wall, the cell immediately to its East must have an open West wall. This behavior is ensured by sharing same instances of `Wall`'s between the cells in a grid.

# Output File

The generated maze is saved to the file specified by `OUTPUT_FILE`.

## Format

The first section contains one hexadecimal digit per cell. After the maze data, there is an empty line followed by:

1.  Entry coordinates.
2.  Exit coordinates.
3.  Shortest path.

Example:

    F9A3
    C05E
    B7D1

    0,0
    19,14
    EESSSWWNEE...

# Visual Representation

This package provides a visual representation of the generated maze using **AsciiRenderer** (terminal ASCII).

The display shows:

- Maze configuration.
- Maze grid (possibly with 42 pattern).
- Entry.
- Exit.
- Display options.

## `"42"` Pattern

The maze contains a visible `"42"` pattern formed using fully closed cells.

For maze dimensions that are too small to contain the pattern, the program displays an error message.

# Reusable Code

## MazeGenerator

The maze-generation logic is implemented as a standalone reusable class:

```python
from mazegen import MazeGenerator
```

The reusable component is responsible for:

- Creating the maze.
- Generating the maze structure.
- Applying the selected algorithm.
- Providing access to the generated maze.
- Providing access to a solution/path.
- Providing a default rendering.

## Basic Example

```python
from mazegen import MazeGenerator, MazeError

try:
    maze = MazeGenerator(
        config_path="config.txt",
    )
except MazeError:
    ...

maze.render()
```

## Customizing the Maze Operators

```python
from mazegen import MazeGenerator, Solver

class CustomSolver(Solver):
    ...

maze = MazeGenerator(
    config_path="config.txt",
)

# Passing your own custom solver abstract class
maze.operators.solver = CustomSolver

maze.render()
```

# Team

- **cbozkurt** | Cahit Atilla Bozkurt (cahitatillabozkurt@gmail.com)

- **adede** | Ahmet Yasin Dede (ahmetyasindd@gmail.com)

## Responsibilities

### **cbozkurt**

- Maze-generation algorithm.
- Visual representation.
- User interaction.
- Output formatting.

### **adede**

- Configuration parsing.
- Constructing reusable models and interfaces.
- Module organization.

# Resources

## Maze Creation

- [Maze Generation Algorithms Wiki](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Maze Solvers Wiki](https://en.wikipedia.org/wiki/Maze-solving_algorithm)
- [Breadth First Search (BFS) Visualization](https://see-algorithms.com/graph/BFS)

## Maze Rendering

- [Unicode Characters Reference](https://www.w3.org/TR/xml-entity-names/025.html)
- [MLX (MiniLibX)](https://harm-smits.github.io/42docs/libs/minilibx.html)
- [`curses` Library Docs](https://docs.python.org/3/howto/curses.html)
- [Terminal Coloring for `curses`](https://stackoverflow.com/questions/18551558/how-to-use-terminal-color-palette-with-curses)

## Code Maintenance

- [PEP 257](https://peps.python.org/pep-0257/)
- [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- [Markdown Cheatsheet](https://www.markdownguide.org/cheat-sheet/)
- [Open Source Licenses Reference](https://choosealicense.com/licenses/)

## AI Usage

AI was used to suggest small implementation ideas and explain algorithms besides the online tools. Generated suggestions were reviewed, tested, modified, and integrated **manually**. No AI was used to generate the code **directly**; all functions were personally implemented.

# License

The selected license explicitly permits reuse and distribution of the package by future projects under some conditions specified in the `LICENSE.md` located at this package's root.

---

42 Kocaeli
