from algorithms import GreedyTspSolver, RandomTspSolver


print("Greedy TSP problem solver:")
greedy_solver = GreedyTspSolver()
greedy_solver.solve()

print("Randomized TSP problem solver:")
random_solver = RandomTspSolver()
random_solver.solve()
