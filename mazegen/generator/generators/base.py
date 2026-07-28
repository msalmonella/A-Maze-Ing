from abc import ABC, abstractmethod
import mazegen


class Generator(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator, seed: str = "") -> None:
        pass
