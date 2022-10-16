from .base import BaseTspSolver
import typing as t
from models import Vertex, Instance
import random
import numpy as np
from utils import time_counter


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
    EVALUATION_DECIMAL_PRECISION = 10

    def __init__(self, instance: Instance, adj_matrix: np.ndarray, solver_config: dict):
        super().__init__(instance, adj_matrix, solver_config)

        self._population_size = self._config.get("population_size", 100)
        self._tournament_size = self._config.get("tournament_size", 5)
        self._number_of_tournaments = self._config.get("number_of_tournaments", 20)
        self._max_num_of_gen = self._config.get("max_number_of_generations", 100)

        self._mutation = self._config.get("mutation", "swap")
        self._mutation_probability = self._config.get("mutation_probability", 0.1)
        self._selection = self._config.get("selection", "tournament")

    @time_counter
    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        # * init vars
        current_num_of_gen = 0
        best_specimen = None
        best_cost = np.Inf

        population = self._initialization(self.instance)  # init generation
        evaluation = self._evaluation(population)

        while not self._stop_condition_achieved(current_num_of_gen):

            temp_cost, temp_specimen = self._select_best_specimen_from_population(population)
            if temp_cost < best_cost:
                best_cost = temp_cost
                best_specimen = temp_specimen

            # * selection
            tournament_winners = []
            for _ in range(self._number_of_tournaments):
                winner_specimen = self._selection_tournament(population, evaluation)
                tournament_winners.append(winner_specimen)

            # * crossover
            new_population = []
            while len(new_population) < self._population_size:
                selected_winners = random.sample(tournament_winners, 2)
                child = self._crossover_ordered(selected_winners[0], selected_winners[1])[0]
                new_population.append(child)

            population = new_population

            # * mutation
            for idx, specimen in enumerate(population):
                if self._should_mutate():
                    population[idx] = self._mutation_swap(specimen)

            # * evaluation
            evaluation = self._evaluation(population)
            current_num_of_gen += 1

        print(f"Best cost: {best_cost}")
        print(f"Best specimen: {best_specimen}")
        return best_cost, best_specimen

    def _should_mutate(self) -> bool:
        return random.random() < self._mutation_probability

    def _select_best_specimen_from_population(self, population: t.List[t.List[Vertex]]) -> t.Tuple[int, t.List[Vertex]]:
        best_specimen = None
        best_cost = np.Inf
        for specimen in population:
            current_cost = self._calculate_total_distance(specimen)
            if current_cost < best_cost:
                best_specimen = specimen
                best_cost = current_cost
        return best_cost, best_specimen

    def _stop_condition_achieved(self, current_num_of_gen) -> bool:
        # TODO maybe add other stop conditions
        if current_num_of_gen >= self._max_num_of_gen:
            return True
        return False

    def _initialization(self, instance: Instance) -> t.List[t.List[Vertex]]:
        init_population = []
        for _ in range(0, self._population_size):
            specimen = self._generate_random_route()
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

    def _crossover_ordered(self, specimen_1: t.List[Vertex], specimen_2: t.List[Vertex]) -> t.List[t.List[Vertex]]:
        children: t.List[t.List[Vertex]] = []
        for _ in range(2):
            child: t.List[Vertex] = [None] * self.instance.dimension
            random_ints: t.List[int] = random.sample(range(0, len(specimen_1)), 2)
            random_ints.sort()
            child[random_ints[0]:random_ints[1]] = specimen_1[random_ints[0]:random_ints[1]]
            child_none_indices = [i for i in range(len(child)) if child[i] is None]
            for vertex in specimen_2:
                if vertex in child:
                    continue
                child[child_none_indices[0]] = vertex
                child_none_indices.pop(0)
            children.append(child)
        return children

    def _crossover_partially_matched(self, specimen_1: t.List[Vertex], specimen_2: t.List[Vertex]) -> t.List[Vertex]:
        pass

    def _mutation_swap(self, to_mutate: t.List[Vertex]) -> t.List[Vertex]:
        random_ints: t.List[int] = random.sample(range(0, self.instance.dimension), 2)
        random_ints.sort()
        to_mutate[random_ints[0]], to_mutate[random_ints[1]] = to_mutate[random_ints[1]], to_mutate[random_ints[0]]
        return to_mutate

    def _mutation_inversion(self, to_mutate: t.List[Vertex]) -> t.List[Vertex]:
        random_ints: t.List[int] = random.sample(range(0, self.instance.dimension), 2)
        random_ints.sort()
        to_mutate[random_ints[0]:random_ints[1]] = to_mutate[random_ints[0]:random_ints[1]][::-1]
        return to_mutate
