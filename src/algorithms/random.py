from models import Vertex, Instance
import numpy as np
import typing as t
from .base import BaseTspSolver
from utils import time_counter


class RandomTspSolver(BaseTspSolver):

    def __init__(self, instance: Instance, solver_config: dict):
        super().__init__(instance, solver_config)
        self._random_repeat = self._config.get("random_repeat", 1000000)

    @time_counter
    def solve(self):
        min_distance = np.Inf
        min_route: t.List[Vertex]

        for _ in range(self._random_repeat):
            generated_route = self._generate_random_route(self.instance)
            total_distance = self._calculate_total_distance(generated_route)

            if total_distance < min_distance:
                min_distance = total_distance
                min_route = generated_route

        return min_distance, min_route
