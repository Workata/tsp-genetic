# from loaders import InstanceLoader

# loader = InstanceLoader()

# instance = loader.load("./instances/ali535.tsp")

# print(instance.dimension)
# print(instance.vertices[4])

from algorithms import GreedyTspSolver
from algorithms import RandomTspSolver

print("Greedy TSP problem solver:")
greedy_solver = GreedyTspSolver()
greedy_solver.solve()

print("Randomized TSP problem solver:")
random_solver = RandomTspSolver()
random_solver.solve()
