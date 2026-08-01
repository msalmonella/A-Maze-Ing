from mlx import Mlx
import mazegen
from . import Renderer
from ..models import Path


class MlxRenderer(Renderer):
    CELL_SIZE = 40
    WALL_THICKNESS = 3

    def func() -> None:
        print("hello, world")
        return
