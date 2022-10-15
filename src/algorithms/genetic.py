from .base import BaseTspSolver
import typing as t
from models import Vertex


class GeneticTspSolver(BaseTspSolver):

    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        pass