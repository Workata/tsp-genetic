from algorithms import GreedyTspSolver, RandomTspSolver, GeneticTspSolver
from loaders import ConfigLoader, InstanceLoader
from utils import Calculator, AdjencyMatrixCreator


CONFIG_FILE_PATH = './config.json'

config = ConfigLoader.load(CONFIG_FILE_PATH)
instance_loader = InstanceLoader()

algorithm = config.get('algorithm')
repetitions = config.get('repetitions')
instance_file_path = config.get('instance_file_path')

# * create instance and adjency matrix
instance = instance_loader.load(instance_file_path)
adj_matrix = AdjencyMatrixCreator(calculator=Calculator()).create(instance)


SOLVERS = {
    "greedy": GreedyTspSolver(instance, adj_matrix, solver_config=config.get('greedy')),
    "genetic": GeneticTspSolver(instance, adj_matrix, solver_config=config.get('genetic')),
    "random": RandomTspSolver(instance, adj_matrix, solver_config=config.get('random'))
}

solver = SOLVERS[algorithm]


# * run solver
for i in range(1, repetitions+1):
    print(f"\n[INFO] ------------------- ITERATION {i} START -----------------")
    print(f"[INFO] TSP problem solver ({algorithm})")
    best_cost, best_route = solver.solve()
    print(f"[INFO] Best cost: {best_cost}")
    print(f"[INFO] Best route: {best_route}")
    print(f"[INFO] ------------------- ITERATION {i} END -------------------\n")


# * save results in csv file
output_file_path = config.get('output_file_path')
solver.output_df.to_csv(output_file_path)
