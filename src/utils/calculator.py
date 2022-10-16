from models import Vertex
import math


class Calculator:

    def calculate_distance_between_vertices(self, vertex_a: Vertex, vertex_b: Vertex) -> int:
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
        return round(math.sqrt(pow(x_diff, 2) + pow(y_diff, 2)))
