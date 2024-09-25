import random
import math
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class GrasshopperOptimizationAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, c_min=0.00004, c_max=1, **kwargs):
        """
        Grasshopper Optimization Algorithm (GOA) implementation.

        :param c_min: Minimum value of the control parameter.
        :param c_max: Maximum value of the control parameter.
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Grasshopper Optimization Algorithm"
        self.c_min = c_min
        self.c_max = c_max
        self.current_iteration = 0  # Initialize current_iteration here

    def s_function(self, x):
        """Attractive/repulsive function (s-function) that controls grasshopper interaction."""
        f = 0.5
        l = 1.5
        return f * math.exp(-x / l) - math.exp(-x)

    def update(self):
        """Update the positions of the grasshoppers."""
        c = self.c_max - self.current_iteration * ((self.c_max - self.c_min) / self.epochs)  # Control parameter

        new_population = []
        for i in range(self.population_size):
            individual = self.population[i]
            new_position = [0.0] * self.solution_vector_size

            for j in range(self.population_size):
                if i != j:
                    dist = self.euclidean_distance(individual.values, self.population[j].values)
                    if dist > 0:  # Avoid division by zero
                        s_ij = self.s_function(dist)
                        for d in range(self.solution_vector_size):
                            new_position[d] += c * s_ij * (self.population[j].values[d] - individual.values[d]) / dist

            # Apply bounds to the new position
            for d in range(self.solution_vector_size):
                new_position[d] = max(self.solution_vector[d]['lower_bound'], min(self.solution_vector[d]['upper_bound'], new_position[d]))

            new_individual = Individual(i, new_position)
            new_population.append(new_individual)

        self.population = new_population

        # Re-evaluate the population and sort
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update the best and global best solutions
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value

    def run(self):
        """Run the algorithm."""
        self.initialize_population()  # Initialize population
        self.evaluate_all_objectives()  # Evaluate initial population

        # Set the initial best solution and objective value
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        self.global_best_solution = self.population[0].values
        self.global_best_objective_value = self.population[0].objective_value

        for epoch_index in range(1, self.epochs + 1):
            self.current_iteration = epoch_index  # Track the current iteration here
            self.update()

            # Log the progress
            print(f'{self.optimizer_name} (pop:{len(self.population)}) |'
                  f' Epoch #{epoch_index}: Current best:{self.best_objective_value}'
                  f' Global best:{self.global_best_objective_value}')

            if self.target_objective_value is not None and self.best_objective_value == self.target_objective_value:
                print(f"Target Objective Value ({self.best_objective_value}) reached before end of all iterations.")
                break

            if self.target_objective_lower_bound is not None and self.best_objective_value >= self.target_objective_lower_bound:
                print(f"Target Objective lower bound ({self.best_objective_value}) reached before end of all iterations.")
                break

            if self.target_objective_upper_bound is not None and self.best_objective_value <= self.target_objective_upper_bound:
                print(f"Target Objective upper bound ({self.best_objective_value}) reached before end of all iterations.")
                break
    def euclidean_distance(self, pos1, pos2):
        """Calculate the Euclidean distance between two positions."""
        return math.sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(pos1, pos2)))
