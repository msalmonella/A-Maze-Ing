from abc import ABC, abstractmethod
import mazegen


class Strategy(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator, seed: str = "") -> None:
        pass
