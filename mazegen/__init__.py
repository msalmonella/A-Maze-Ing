"""Tools for working with a maze.

This package exposes the main `MazeGenerator` class and helper methods for
creating and processing a maze.

Operations such as `Solver`s or `Renderer`s can be passed down from the maze's
`operations` attribute to customize the maze's behavior further.
"""

from .maze_generator import MazeGenerator
from .errors import MazeError

from .algorithms import Algorithm
from .solvers import Solver
from .renderers import Renderer

__all__ = ["MazeGenerator", "MazeError", "Algorithm", "Solver", "Renderer"]
