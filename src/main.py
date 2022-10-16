from algorithms import GreedyTspSolver, RandomTspSolver, GeneticTspSolver
from loaders import ConfigLoader, InstanceLoader


CONFIG_FILE_PATH = './config.json'

config = ConfigLoader.load(CONFIG_FILE_PATH)

instance_loader = InstanceLoader()
instance =  instance_loader.load(config.get('instance_file_path'))

print(config)

SOLVERS = {
    "greedy": GreedyTspSolver(instance, solver_config=config.get('greedy')),
    "genetic": GeneticTspSolver(instance, solver_config=config.get('genetic')),
    "random": RandomTspSolver(instance, solver_config=config.get('random'))
}

algorithm = config.get('algorithm')
solver = SOLVERS[algorithm]
print(f"{algorithm} TSP problem solver:")
solver.solve()
