from .base import BaseTspSolver
import typing as t
from models import Vertex, Instance
import random
import numpy as np
from utils import time_counter
import math


class GeneticTspSolver(BaseTspSolver):
    """
    fitness function: f(total_cost) = 1/total_cost

    mutation:
        - swap
        - inversion

    selection:
        - tournament
        - roulette

    crossover:
        - ordered
        - partially matched
    """
    EVALUATION_DECIMAL_PRECISION = 10

    def __init__(self, instance: Instance, adj_matrix: np.ndarray, solver_config: dict):
        super().__init__(instance, adj_matrix, solver_config)

        self._population_size = self._config.get("population_size", 100)
        self._tournament_size = self._config.get("tournament_size", 5)
        self._number_of_tournaments = self._config.get("number_of_tournaments", 20)
        self._max_num_of_gen = self._config.get("max_number_of_generations", 100)

        self._mutation_type = self._config.get("mutation", "swap")
        self._mutation_probability = self._config.get("mutation_probability", 0.1)
        self._selection_type = self._config.get("selection", "tournament")
        self._crossover_type = self._config.get("crossover", "ordered")

    @time_counter
    def solve(self) -> t.Tuple[int, t.List[Vertex]]:
        current_num_of_gen = 0
        best_specimen = None
        best_cost = np.Inf

        population = self._initialization()  # init generation
        evaluation = self._evaluation(population)

        while not self._stop_condition_achieved(current_num_of_gen):

            temp_cost, temp_specimen = self._select_best_specimen_from_population(population)
            if temp_cost < best_cost:
                best_cost = temp_cost
                best_specimen = temp_specimen

            # * selection
            selected_specimens = self._selection(population, evaluation)

            # * crossover
            population = self._crossover(selected_specimens)

            # * mutation
            population = self._mutation(population)

            # * evaluation
            evaluation = self._evaluation(population)
            current_num_of_gen += 1

        return best_cost, best_specimen

    def _selection(self, population: t.List[t.List[Vertex]], evaluation: t.List[float]) -> t.List[t.List[Vertex]]:
        selected_specimens = []
        if self._selection_type == 'tournament':
            for _ in range(self._number_of_tournaments):
                selected_specimen = self._selection_tournament(population, evaluation)
                selected_specimens.append(selected_specimen)
        elif self._selection_type == 'roulette':
            for _ in range(self._population_size):
                selected_specimen = self._selection_roulette(population, evaluation)
                selected_specimens.append(selected_specimen)
        else:
            raise NotImplementedError
        return selected_specimens

    def _crossover(self, selected_specimens: t.List[t.List[Vertex]]) -> t.List[t.List[Vertex]]:
        new_population = []

        while len(new_population) < self._population_size:
            parents = random.sample(selected_specimens, 2)
            if self._crossover_type == 'ordered':
                child = self._crossover_ordered(parents[0], parents[1])[0]
            elif self._crossover_type == 'partially_matched':
                # TODO implement partially matched
                child = self._crossover_partially_matched(parents[0], parents[1])[0]
            else:
                raise NotImplementedError
            new_population.append(child)
        return new_population

    def _mutation(self, population: t.List[t.List[Vertex]]) -> t.List[t.List[Vertex]]:
        for idx, specimen in enumerate(population):
            if self._should_mutate():
                if self._mutation_type == 'swap':
                    population[idx] = self._mutation_swap(specimen)
                elif self._mutation_type == 'inversion':
                    population[idx] = self._mutation_inversion(specimen)
                else:
                    raise NotImplementedError
        return population

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
        if current_num_of_gen >= self._max_num_of_gen:
            return True
        return False

    def _initialization(self) -> t.List[t.List[Vertex]]:
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
            total_cost = self._calculate_total_distance(specimen)
            # * 1/x OR 1 / math.log(1+x)
            rating = round(
                1 / math.log(1 + total_cost),
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

    def _selection_roulette(self, population: t.List[t.List[Vertex]], evaluation: t.List[float]) -> t.List[Vertex]:
        evaluation_sum = sum(evaluation)
        probability_rate_all = [eva / evaluation_sum for eva in evaluation]
        evaluation_indexes_mapping = sorted(range(len(probability_rate_all)), key=lambda k: probability_rate_all[k],
                                            reverse=True)
        sorted_probability_rate_all = sorted(probability_rate_all, reverse=True)
        probability_inflow = sorted_probability_rate_all

        for i in range(len(sorted_probability_rate_all)):
            if i == 0:
                continue
            elif i == len(sorted_probability_rate_all) - 1:
                probability_inflow[i] = 1
            else:
                probability_inflow[i] += probability_inflow[i - 1]

        toss = random.random()
        for i in range(len(probability_inflow)):
            if toss <= probability_inflow[i]:
                return population[evaluation_indexes_mapping[i]]
        raise Exception('If this happened then selection_roulette has a bug :)')

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

    def _crossover_partially_matched(self, specimen_1: t.List[Vertex], specimen_2: t.List[Vertex]) -> t.List[t.List[Vertex]]:
        random_ints: t.List[int] = random.sample(range(0, self.instance.dimension), 2)
        random_ints.sort()

        specimen_1_part: t.List[Vertex] = specimen_1[random_ints[0]:random_ints[1]]
        specimen_2_part: t.List[Vertex] = specimen_2[random_ints[0]:random_ints[1]]
        exchange_matrix = np.zeros((2, len(specimen_1_part)), dtype=Vertex)
        exchange_matrix[0], exchange_matrix[1] = specimen_2_part, specimen_1_part

        child_1: t.List[Vertex] = [None] * self.instance.dimension
        child_2: t.List[Vertex] = [None] * self.instance.dimension
        child_1[random_ints[0]:random_ints[1]] = specimen_2_part
        child_2[random_ints[0]:random_ints[1]] = specimen_1_part

        mapping_list: t.List[t.List[Vertex]] = []
        stop_mapping_condition = True
        mapped_vertex: Vertex = None
        for i in range(len(specimen_1_part)):
            mapped_vertex = specimen_2_part[i]
            stop_mapping_condition = True
            while stop_mapping_condition:
                if mapped_vertex in specimen_2_part:
                    index_list_to_append: int = None
                    for sublist in mapping_list:
                        if mapped_vertex in sublist:
                            index_list_to_append = mapping_list.index(sublist)
                            continue
                    if index_list_to_append is not None:
                        list_to_append: t.List[Vertex] = mapping_list[index_list_to_append]
                    else:
                        list_to_append: t.List[Vertex] = []
                    if not list_to_append:
                        list_to_add: t.List[Vertex] = [mapped_vertex, specimen_1_part[i]]
                        mapping_list.append(list_to_add)
                        mapped_vertex = specimen_1_part[i]
                    else:
                        mapped_vertex_index: int = specimen_2_part.index(mapped_vertex)
                        if specimen_1_part[mapped_vertex_index] not in list_to_append:
                            list_to_append.append(specimen_1_part[mapped_vertex_index])
                            mapping_list[index_list_to_append] = list_to_append
                            mapped_vertex = specimen_1_part[mapped_vertex_index]
                        else:
                            stop_mapping_condition = False
                else:
                    stop_mapping_condition = False
        children: t.List[t.List[Vertex]] = [self._map_child(child_1, specimen_1, mapping_list),
                                            self._map_child(child_2, specimen_2, mapping_list)]
        return children

    def _map_child(self, child, parent, mapping_list) -> t.List[Vertex]:
        for i in range(self.instance.dimension):
            if child[i] is None:
                found_list = [list_value for list_value in mapping_list if parent[i] in list_value]
                if found_list:
                    found_list = found_list[0]
                    if parent[i] == found_list[0]:
                        child[i] = found_list[-1]
                    else:
                        child[i] = found_list[0][0]
                else:
                    child[i] = parent[i]
        return child

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
