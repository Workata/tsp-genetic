import numpy as np
import typing as t
from models import Vertex
from .base import BaseTspSolver


class GreedyTspSolver(BaseTspSolver):
    """
    WIP
    TODO Add BaseSolver - instance loader + adj matrix creator
    TODO Check if this is ok
    TODO decorators - time, csv output?
    """

    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        # berlin11_modified.tsp gr666.tsp
        instance = self._instance_loader.load("./instances/berlin11_modified.tsp")
        adj_matrix = self._matrix_creator.create(instance)

        min_distance: float = np.Inf
        min_route: t.List[Vertex] = None

        for starting_vertex in instance.vertices:
            visited_vertices = [starting_vertex]
            total_cost = 0

            temp_mini = np.Inf
            temp_vertex = None

            while len(visited_vertices) != instance.dimension:
                vertex_a = visited_vertices[-1]  # V_a => recently visited vertex

                temp_mini = np.Inf
                temp_vertex = None

                # * find the lowest cost of V_a -----> V_b connection (edge)
                for vertex_b in instance.vertices:
                    if vertex_b in visited_vertices:
                        continue

                    distance = adj_matrix[vertex_a.number][vertex_b.number]
                    if temp_mini > distance:
                        temp_vertex = vertex_b
                        mini = distance

                visited_vertices.append(temp_vertex)
                total_cost += mini

            # ! add cost of a last edge
            last_vertex = visited_vertices[-1]
            total_cost += adj_matrix[last_vertex.number][starting_vertex.number]
            # ! add starting vertex again
            visited_vertices.append(starting_vertex)

            total_cost = round(total_cost, 2)

            if total_cost < min_distance:
                min_distance = total_cost
                min_route = visited_vertices

        print((min_distance, min_route))

        return min_distance, min_route
