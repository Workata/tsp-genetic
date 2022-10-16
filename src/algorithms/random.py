from models import Vertex
import numpy as np
import typing as t
from .base import BaseTspSolver
from utils import time_counter


class RandomTspSolver(BaseTspSolver):

    @time_counter
    def solve(self):
        min_distance = np.Inf
        min_route: t.List[Vertex]

        for _ in range(100000):
            generated_route = self._generate_random_route(self.instance)
            total_distance = self._calculate_total_distance(generated_route)

            if total_distance < min_distance:
                min_distance = total_distance
                min_route = generated_route

        print((min_distance, min_route))
        return min_distance, min_route
