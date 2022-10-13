from models import Instance, Vertex
import numpy as np
import math


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

    DISTANCE_DECIMAL_PRECISION = 2

    def create(self, instance: Instance) -> np.ndarray:
        num_of_vertices = instance.dimension
        matrix = np.zeros((num_of_vertices + 1, num_of_vertices + 1), dtype=float)

        for vertex_a in instance.vertices:
            for vertex_b in instance.vertices:
                if vertex_a == vertex_b:
                    continue

                distance = self._calculate_distance_between_vertices(vertex_a, vertex_b)
                # symmetric adjacency matrix
                matrix[vertex_a.number][vertex_b.number] = distance
                matrix[vertex_b.number][vertex_a.number] = distance

        return matrix



    def _calculate_distance_between_vertices(self, vertex_a: Vertex, vertex_b: Vertex) -> float:
        """
        Equation:
        A = (x_1, y_1), B = (x_2, y_2)
        |AB| = sqrt( (x_2 - x_1)^2 + (y_2 - y_1)^2 )

        Args:
            vertex_a (Vertex): first point (vertex)
            vertex_b (Vertex): second point (vertex)

        Returns:
            float: Distance between two given points (vertices) - rounded to given decimal precision
        """
        x_diff = vertex_a.x - vertex_b.x
        y_diff = vertex_a.y - vertex_b.y
        return round( math.sqrt(pow(x_diff, 2) + pow(y_diff, 2)), self.DISTANCE_DECIMAL_PRECISION )
