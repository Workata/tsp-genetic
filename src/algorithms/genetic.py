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
    EVALUATION_DECIMAL_PRECISION = 6

    def __init__(self, instance: Instance, solver_config: dict):
        super().__init__(instance, solver_config)
        self._population_size = self._config.get("population_size", 100)
        self._tournament_size = self._config.get("tournament_size", 5)
        self._number_of_tournaments = self._config.get("number_of_tournaments", 20)
        self._max_num_of_gen = self._config.get("max_number_of_generations", 100)

        self._mutation = self._config.get("mutation")
        self._selection = self._config.get("selection")


    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        total_cost = None
        path = []

        current_num_of_gen = 0

        population = self._initialization(self._instance)  # init generation
        # print(population)
        evaluation = self._evaluation(population)
        # print(evaluation)

        while not self._stop_condition_achieved(current_num_of_gen):
            self._selection_tournament(population, evaluation)
            self._crossover()
            population = self._mutation_swap(population)
            evaluation = self._evaluation(population)
            current_num_of_gen += 1

        return total_cost, path

    def _stop_condition_achieved(self, current_num_of_gen) -> bool:
        # TODO maybe add other stop conditions
        if current_num_of_gen >= self._max_num_of_gen:
            return True
        return False

    def _initialization(self, instance: Instance) -> t.List[t.List[Vertex]]:
        init_population = []
        for _ in range(0, self._population_size):
            specimen = self._generate_random_route(instance)
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
            rating = round(
                1 / self._calculate_total_distance(specimen),
                self.EVALUATION_DECIMAL_PRECISION
            )
            ratings.append(rating)
        return ratings

    def _selection_tournament(self, population: t.List[t.List[Vertex]], evaluation: t.List[float]) -> t.List[Vertex]:
        best_rating = -1
        best_specimen_index = None
        selected_specimens_indexes = random.sample(range(self._population_size), self._tournament_size)

        for specimen_index in selected_specimens_indexes:
            if best_rating < evaluation[specimen_index]:
                best_specimen_index = specimen_index
                best_rating = evaluation[specimen_index]

        return population[best_specimen_index]

    def _selection_roulette(self):
        pass

    def _crossover_ordered(self, specimen_1: t.List[Vertex], specimen_2: t.List[Vertex]) -> t.List[Vertex]:
        child: t.List[Vertex] = [None] * len(specimen_1)
        random_ints: t.List[int] = random.sample(range(0, len(specimen_1)), 2)
        if random_ints[0] > random_ints[1]:
            child[random_ints[1]:random_ints[0]] = specimen_1[random_ints[1]:random_ints[0]]
        else:
            child[random_ints[0]:random_ints[1]] = specimen_1[random_ints[0]:random_ints[1]]

        child_none_indices = [i for i in range(len(child)) if child[i] is None]
        for vertex in specimen_2:
            if vertex in child:
                continue
            child[child_none_indices[0]] = vertex
            child_none_indices.pop(0)
        return child

    def _mutation_swap(self, to_mutate: t.List[Vertex]) -> t.List[Vertex]:
        random_ints: t.List[int] = random.sample(range(0, len(to_mutate) - 1), 2)
        to_mutate[random_ints[0]], to_mutate[random_ints[1]] = to_mutate[random_ints[1]], to_mutate[random_ints[0]]
        return to_mutate

    def _mutation_inversion(self, to_mutate: t.List[Vertex]) -> t.List[Vertex]:
        random_ints: t.List[int] = random.sample(range(0, len(to_mutate)), 2)
        if random_ints[0] > random_ints[1]:
            to_mutate[random_ints[1]:random_ints[0]] = to_mutate[random_ints[1]:random_ints[0]][::-1]
        else:
            to_mutate[random_ints[0]:random_ints[1]] = to_mutate[random_ints[0]:random_ints[1]][::-1]
        return to_mutate
