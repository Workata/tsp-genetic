from abc import abstractmethod, ABC
import typing as t
from models import Vertex, Instance
import random
import pandas as pd
import numpy as np


class BaseTspSolver(ABC):

    DISTANCE_DECIMAL_PRECISION = 2

    def __init__(self, instance: Instance, adj_matrix: np.ndarray, solver_config: dict):
        self._config = solver_config
        self._adj_matrix = adj_matrix

        # instance is public - needed for output
        self.instance = instance
        self.output_df = pd.DataFrame()


    @abstractmethod
    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        pass


    def _generate_random_route(self) -> t.List[Vertex]:
        new_route = self.instance.vertices.copy()
        random.shuffle(new_route)
        return new_route

    def _calculate_total_distance(self, route: t.List[Vertex]) -> float:
        total_distance: float = 0.0
        for i in range(len(route) - 1):
            total_distance += self._adj_matrix[route[i].number][route[i + 1].number]
        total_distance += self._adj_matrix[route[-1].number][route[0].number]
        return round(total_distance, self.DISTANCE_DECIMAL_PRECISION)
