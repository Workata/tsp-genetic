from loaders import InstanceLoader
import numpy as np
from utils import AdjencyMatrixCreator

class GreedyTspSolver():
    """
    WIP
    TODO Add BaseSolver - instance loader + adj matrix creator
    TODO Check if this is ok
    TODO decorators - time, csv output?
    """

    def solve(self,):
        loader = InstanceLoader()
        # berlin11_modified.tsp gr666.tsp
        instance = loader.load("./instances/berlin11_modified.tsp")
        matrix_creator = AdjencyMatrixCreator()
        adj_matrix = matrix_creator.create(instance)


        starting_vertex = instance.vertices[0]
        visited_vertices = [starting_vertex]
        total_cost = 0

        temp_mini = np.Inf
        temp_vertex = None

        while len(visited_vertices) != instance.dimension:
            vertex_a = visited_vertices[-1]     # V_a => recently visited vertex

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

        print((total_cost, visited_vertices))

        return total_cost, visited_vertices
