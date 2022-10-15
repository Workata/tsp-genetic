from re import L
from .base import BaseTspSolver
import typing as t
from models import Vertex, Instance
import random


class GeneticTspSolver(BaseTspSolver):
    """
    fitness function: f(total_cost) = 1/total_cost

    mutation:
        - swap
        - inversion

    selection:
        - tournament
        - roulette
    """
    POPULATION_SIZE = 5   # default 100
    TOURNAMENT_SIZE = 1   # default 5
    MAX_NUM_OF_GEN = 100  # default 100

    EVALUATION_DECIMAL_PRECISION = 6

    def solve(self) -> t.Tuple[int, t.List[Vertex]]:

        total_cost = None
        path = []

        instance = self._instance_loader.load("./instances/berlin11_modified.tsp")
        current_num_of_gen = 0

        population = self._initialization(instance)     # init generation
        # print(population)
        evaluation = self._evaluation(population)
        # print(evaluation)

        while not self._stop_condition_achieved(current_num_of_gen):
            self._selection_tournament(population, evaluation)
            self._crossover()
            self._mutation_swap()
            self._evaluation(population)
            current_num_of_gen += 1

        return total_cost, path



    def _stop_condition_achieved(self, current_num_of_gen) -> bool:
        # TODO maybe add other stop conditions
        if current_num_of_gen >= self.MAX_NUM_OF_GEN:
            return True
        return False

    def _initialization(self, instance: Instance) -> t.List[ t.List[Vertex] ]:
        init_population = []
        for _ in range(0, self.POPULATION_SIZE):
            specimen = self._generate_random_route(instance, add_last_vertex = False)
            init_population.append(specimen)
        return init_population

    def _evaluation(self, population: t.List[t.List[Vertex]]) -> t.List[float]:
        """
        Get a specimen evaluation based on "Fitness Function"

        Possible fitness functions:
            - 1 / total_cost
            - log(1+x) !!! shouldn't this be 1/log(1+x) ???
            TODO probably change for log

        Args:
            specimen (t.List[Vertex]): _description_

        Returns:
            float: value of choosen fitness function
        """
        ratings = []
        for specimen in population:
            rating = round(1 / self._calculate_total_distance(specimen), self.EVALUATION_DECIMAL_PRECISION)
            ratings.append(rating)
        return ratings

    def _selection_tournament(self, population: t.List[t.List[Vertex]], evaluation: t.List[float]) -> t.List[Vertex]:
        best_rating = -1
        best_specimen_index = None
        selected_specimens_indexes = random.sample(range(self.POPULATION_SIZE), self.TOURNAMENT_SIZE)

        for specimen_index in selected_specimens_indexes:
            if best_rating < evaluation[specimen_index]:
                best_specimen_index = specimen_index
                best_rating = evaluation[specimen_index]

        return population[best_specimen_index]

    def _selection_roulette(self):
        pass

    def _crossover(self):
        pass

    def _mutation_swap(self):
        pass

    def _mutation_inversion(self):
        pass