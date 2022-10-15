from abc import abstractmethod, ABC
import typing as t
from utils import Calculator, AdjencyMatrixCreator
from models import Vertex
from loaders import InstanceLoader
from models import Instance
import random


class BaseTspSolver(ABC):

    def __init__(self):
        self._instance_loader = InstanceLoader()
        self._calculator = Calculator()
        self._matrix_creator = AdjencyMatrixCreator(calculator=self._calculator)

    @abstractmethod
    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        pass

    def _generate_random_route(self, instance: Instance, add_last_vertex: bool = True) -> t.List[Vertex]:
        new_route = instance.vertices.copy()
        random.shuffle(new_route)
        if add_last_vertex:
            new_route.append(new_route[0])
        return new_route

    def _calculate_total_distance(self, route: t.List[Vertex], route_with_last_vertex: bool = True) -> int:
        total_distance: float = 0.0
        for i in range(len(route) - 1):
            total_distance += self._calculator.calculate_distance_between_vertices(route[i], route[i+1])
        if not route_with_last_vertex:
            total_distance += self._calculator.calculate_distance_between_vertices(route[-1], route[0])
        return round(total_distance, 2)
