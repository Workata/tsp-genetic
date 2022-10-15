from models import Instance
from models import Vertex
import numpy as np
import typing as t
import random
from .base import BaseTspSolver

class RandomTspSolver(BaseTspSolver):
    instance: Instance

    def solve(self):
        # berlin11_modified.tsp gr666.tsp
        instance = self._instance_loader.load("./instances/berlin11_modified.tsp")
        self.instance = instance
        min_distance = np.Inf
        min_route: t.List[Vertex]

        for _ in range(100000):
            generated_route = self._generate_route()
            total_distance = self._calculate_total_distance(generated_route)

            if total_distance < min_distance:
                min_distance = total_distance
                min_route = generated_route

        print((min_distance, min_route))
        return min_distance, min_route

    def _generate_route(self) -> t.List[Vertex]:
        new_route = self.instance.vertices.copy()
        random.shuffle(new_route)
        new_route.append(new_route[0])
        return new_route

    def _calculate_total_distance(self, route: t.List[Vertex]):
        total_distance: float = 0.0
        for i in range(len(route) - 1):
            total_distance += self._calculator.calculate_distance_between_vertices(route[i], route[i + 1])
        return round(total_distance, 2)
