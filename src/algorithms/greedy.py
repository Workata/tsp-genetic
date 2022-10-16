import numpy as np
import typing as t
from models import Vertex
from .base import BaseTspSolver
import time


class GreedyTspSolver(BaseTspSolver):
    """
    WIP
    TODO Improve SPEED! !!
    TODO decorators - time, csv output?
    """

    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        adj_matrix = self._matrix_creator.create(self._instance)

        best_cost: float = np.Inf
        best_route: t.List[Vertex] = None

        start = time.time_ns()

        for starting_vertex in self._instance.vertices:
            visited_vertices = [starting_vertex]
            total_cost = 0

            temp_mini = np.Inf
            temp_vertex = None

            while len(visited_vertices) != self._instance.dimension:
                vertex_a = visited_vertices[-1]  # V_a => recently visited vertex

                temp_mini = np.Inf
                temp_vertex = None

                # * find the lowest cost of V_a -----> V_b connection (edge)
                for vertex_b in self._instance.vertices:
                    if vertex_b in visited_vertices:
                        continue

                    distance = adj_matrix[vertex_a.number][vertex_b.number]
                    if temp_mini > distance:
                        temp_vertex = vertex_b
                        temp_mini = distance

                visited_vertices.append(temp_vertex)
                total_cost += temp_mini

            # ! add cost of a last edge
            last_vertex = visited_vertices[-1]
            total_cost += adj_matrix[last_vertex.number][starting_vertex.number]
            total_cost = round(total_cost, 2)

            if total_cost < best_cost:
                best_cost = total_cost
                best_route = visited_vertices

        end = time.time_ns()
        fin_time = (end-start) / 1000000000
        print("CZASSS")
        print(fin_time)
        # print(min_distance)

        return best_cost, best_route
