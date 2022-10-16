from abc import abstractmethod, ABC
import typing as t
from utils import Calculator, AdjencyMatrixCreator
from models import Vertex, Instance
import random


class BaseTspSolver(ABC):

    DISTANCE_DECIMAL_PRECISION = 2

    def __init__(self, instance: Instance, solver_config: dict):
        self._config = solver_config
        self._instance = instance
        self._calculator = Calculator()
        self._matrix_creator = AdjencyMatrixCreator(calculator=self._calculator)

    @abstractmethod
    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        pass

    def _generate_random_route(self, instance: Instance) -> t.List[Vertex]:
        new_route = instance.vertices.copy()
        random.shuffle(new_route)
        return new_route

    def _calculate_total_distance(self, route: t.List[Vertex]) -> float:
        total_distance: float = 0.0
        for i in range(len(route) - 1):
            total_distance += self._calculator.calculate_distance_between_vertices(route[i], route[i + 1])
        total_distance += self._calculator.calculate_distance_between_vertices(route[-1], route[0])
        return round(total_distance, self.DISTANCE_DECIMAL_PRECISION)
