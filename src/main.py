from algorithms import GreedyTspSolver, RandomTspSolver, GeneticTspSolver
from loaders import ConfigLoader, InstanceLoader

# TODO csv output
# TODO re run - repetitions

CONFIG_FILE_PATH = './config.json'

config = ConfigLoader.load(CONFIG_FILE_PATH)

instance_loader = InstanceLoader()
instance = instance_loader.load(config.get('instance_file_path'))

# print(config)

SOLVERS = {
    "greedy": GreedyTspSolver(instance, solver_config=config.get('greedy')),
    "genetic": GeneticTspSolver(instance, solver_config=config.get('genetic')),
    "random": RandomTspSolver(instance, solver_config=config.get('random'))
}

algorithm = config.get('algorithm')
solver = SOLVERS[algorithm]
print(f"[INFO] TSP problem solver ({algorithm})")
best_cost, best_route = solver.solve()
print(f"[INFO] Best cost: {best_cost}")
print(f"[INFO] Best route: {best_route}")
