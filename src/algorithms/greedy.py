import numpy as np
import typing as t
from models import Vertex
from .base import BaseTspSolver
from utils import time_counter
import copy


class GreedyTspSolver(BaseTspSolver):
    """
    TODO Improve SPEED! !!
    TODO decorators - time, csv output?
    """

    @time_counter
    def solve(self) -> t.Tuple[int, t.List[Vertex]]:

        best_cost: float = np.Inf
        best_route: t.List[Vertex] = None

        for starting_vertex in self.instance.vertices:
            unvisited_vertices = copy.copy(self.instance.vertices)
            visited_vertices = [starting_vertex]

            unvisited_vertices.remove(starting_vertex)
            recently_visited_vertex = starting_vertex
            total_cost = 0

            while unvisited_vertices:
                vertex_a = recently_visited_vertex  # V_a => recently visited vertex

                temp_mini = np.Inf
                temp_vertex = None

                # * find the lowest cost of V_a -----> V_b connection (edge)
                for vertex_b in unvisited_vertices:

                    distance = self._adj_matrix[vertex_a.number][vertex_b.number]
                    if temp_mini > distance:
                        temp_vertex = vertex_b
                        temp_mini = distance

                recently_visited_vertex = temp_vertex
                visited_vertices.append(recently_visited_vertex)
                unvisited_vertices.remove(recently_visited_vertex)
                total_cost += temp_mini

            # ! add cost of a last edge
            total_cost += self._adj_matrix[recently_visited_vertex.number][starting_vertex.number]
            total_cost = round(total_cost, 2)

            if total_cost < best_cost:
                best_cost = total_cost
                best_route = visited_vertices

        return best_cost, best_route
