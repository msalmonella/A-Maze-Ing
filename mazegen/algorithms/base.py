from abc import ABC, abstractmethod
from random import Random
from collections.abc import Generator
import mazegen


class Algorithm(ABC):

    @abstractmethod
    def __call__(
        self, maze: mazegen.MazeGenerator, rng: Random
    ) -> Generator[None]:
        pass
