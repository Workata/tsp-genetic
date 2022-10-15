from algorithms import GreedyTspSolver, RandomTspSolver, GeneticTspSolver


print("Greedy TSP problem solver:")
greedy_solver = GreedyTspSolver()
greedy_solver.solve()

print("Randomized TSP problem solver:")
random_solver = RandomTspSolver()
random_solver.solve()

print("Genetic TSP problem solver:")
genetic_solver = GeneticTspSolver()
genetic_solver.solve()
