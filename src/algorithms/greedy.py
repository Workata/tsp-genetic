from loaders import InstanceLoader
import numpy as np
from utils import AdjencyMatrixCreator

class GreedyTspSolver():
    """
    WIP
    Add BaseSolver - instance loader + adj matrix creator
    """

    def solve(self,):
        loader = InstanceLoader()
        # berlin11_modified.tsp gr666.tsp
        instance = loader.load("./instances/berlin11_modified.tsp")
        matrx_creator = AdjencyMatrixCreator()
        adj_matrix = matrx_creator.create(instance)

        print(adj_matrix)
