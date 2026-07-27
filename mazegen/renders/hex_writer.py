import mazegen
from . import Renderer
from ..generator.models import GridIndex


class HexWriter(Renderer):
    def __call__(
        self, maze: mazegen.MazeGenerator, solution: list[GridIndex]
    ) -> None:
        entry_x, entry_y = maze.entry
        exit_x, exit_y = maze.exit

        with open(maze.output_file, "w") as f:
            print(maze.output_file)
            for row in maze.grid:
                line = ""
                for cell in row:
                    line += hex(cell.value)
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{entry_x},{entry_y}\n")
            f.write(f"{exit_x},{exit_y}\n")
            f.write(f"{"".join(self._nesw_conversion(solution))}")

    def _nesw_conversion(self, path: list[GridIndex]) -> list[str]:
        nesw: list[str] = []
        for i in range(len(path) - 1):
            current = path[i]
            next_cell = path[i + 1]

            current_y, current_x = current
            next_y, next_x = next_cell

            if next_y > current_y:
                nesw.append("N")

            if next_x > current_x:
                nesw.append("E")

            if current_y > next_y:
                nesw.append("S")

            if current_x > next_x:
                nesw.append("W")

        return nesw
