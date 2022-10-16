from models import Instance, Vertex
import numpy as np
import typing as t


class CalculatorInterface(t.Protocol):

    def calculate_distance_between_vertices(self, vertex_a: Vertex, vertex_b: Vertex) -> float:
        pass


class AdjencyMatrixCreator:
    """
        NOTE: first column and row will be blank
        Example output (3 vertices):
        [[   0.    0.    0.    0]
         [   0.    0.  666.  281.]
         [   0.  666.    0.  649.]
         [   0.  281.  649.    0.]
        ]
    """

    def __init__(self, calculator: CalculatorInterface):
        self._calculator = calculator

    def create(self, instance: Instance) -> np.ndarray:
        num_of_vertices = instance.dimension
        matrix = np.zeros((num_of_vertices + 1, num_of_vertices + 1), dtype=float)

        for vertex_a in instance.vertices:
            for vertex_b in instance.vertices:
                if vertex_a == vertex_b:
                    continue

                distance = self._calculator.calculate_distance_between_vertices(vertex_a, vertex_b)

                # symmetric adjacency matrix
                matrix[vertex_a.number][vertex_b.number] = distance

        return matrix
