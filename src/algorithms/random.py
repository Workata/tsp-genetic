from models import Vertex
import numpy as np
import typing as t
from .base import BaseTspSolver

class RandomTspSolver(BaseTspSolver):

    def solve(self):
        # berlin11_modified.tsp gr666.tsp
        instance = self._instance_loader.load("./instances/berlin11_modified.tsp")
        min_distance = np.Inf
        min_route: t.List[Vertex]

        for _ in range(100000):
            generated_route = self._generate_random_route(instance)
            total_distance = self._calculate_total_distance(generated_route)

            if total_distance < min_distance:
                min_distance = total_distance
                min_route = generated_route

        print((min_distance, min_route))
        return min_distance, min_route
