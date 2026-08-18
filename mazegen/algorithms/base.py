from abc import ABC, abstractmethod
from random import Random
import mazegen


class Algorithm(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator, rng: Random) -> None:
        pass
