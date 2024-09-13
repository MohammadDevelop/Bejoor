from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual
from bejoor.genetic import BaseGeneticAlgorithm
import random

class MemeticAlgorithm(BaseGeneticAlgorithm):
    def __init__(self, *args, local_search_iterations=10, **kwargs):
        """
        Memetic Algorithm with local search.
        :param local_search_iterations: Number of local search iterations to improve each solution.
        """
        super().__init__(*args, **kwargs)
        self.local_search_iterations = local_search_iterations
        self.optimizer_name = "Memetic Algorithm"

    def local_search(self, individual):
        """Local search to fine-tune the individual."""
        best_local_solution = individual.get_values()[:]
        best_local_value = self.objective_function(best_local_solution)

        for _ in range(self.local_search_iterations):
            neighbor = best_local_solution[:]
            # Small random perturbation to find a local optimum
            for i in range(self.solution_vector_size):
                if self.solution_vector[i]['type'] == 'integer':
                    neighbor[i] += random.choice([-1, 1])
                    neighbor[i] = min(max(neighbor[i], self.solution_vector[i]['lower_bound']),
                                      self.solution_vector[i]['upper_bound'])
                elif self.solution_vector[i]['type'] == 'float':
                    neighbor[i] += random.uniform(-0.1, 0.1)
                    neighbor[i] = min(max(neighbor[i], self.solution_vector[i]['lower_bound']),
                                      self.solution_vector[i]['upper_bound'])

            neighbor_value = self.objective_function(neighbor)
            if (self.optimization_side == 'min' and neighbor_value < best_local_value) or \
               (self.optimization_side == 'max' and neighbor_value > best_local_value):
                best_local_solution = neighbor
                best_local_value = neighbor_value

        individual.set_objective_value(best_local_value)
        individual.values = best_local_solution

    def update(self):
        """Perform local search after crossover and mutation."""
        super().update()  # Perform genetic operations

        # Apply local search on the population
        for individual in self.population:
            self.local_search(individual)

        # Re-evaluate and sort the population after local search
        self.evaluate_all_objectives()
        self.sort_individuals()
