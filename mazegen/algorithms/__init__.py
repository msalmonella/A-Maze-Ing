"""Built-in algorithms to provide different maze behaviors."""

from .base import Algorithm
from .mazer_the_miner import MazerTheMiner
from .prim import Prim

__all__ = ["Algorithm", "MazerTheMiner", "Prim"]
