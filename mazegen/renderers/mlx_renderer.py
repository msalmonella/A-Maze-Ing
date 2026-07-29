from mlx import Mlx
import mazegen
from . import Renderer
from ..models import Path


class MlxRenderer(Renderer):
    CELL_SIZE = 40
    WALL_THICKNESS = 3

    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        width = maze.width * self.CELL_SIZE
        height = maze.height * self.CELL_SIZE
        m: Mlx
        mlx_ptr: int
        win_ptr: int
        img_ptr: int
        buffer: memoryview
        bpp: int
        size_line: int
        fmt: int
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.win_ptr = self.m.mlx_new_window(self.mlx_ptr, width, height, "A-Maze-ing")

        self.m.mlx_key_hook(self.win_ptr, self._on_key, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self._on_close, None)

        self.m.mlx_loop(self.mlx_ptr)

    def _put_pixel(self, x: int, y: int, color: int) -> None:
        bpp = self.bpp // 8
        offset = y * self.size_line + x * bpp
        self.buffer[offset:offset + bpp] = color.to_bytes(bpp, "little")

    def _on_key(self, keycode: int, param: object) -> None:
        if keycode == 65307:  # Escape key
            self.m.mlx_loop_exit(self.mlx_ptr)

    def _on_close(self, param: object) -> None:
        self.m.mlx_loop_exit(self.mlx_ptr)
