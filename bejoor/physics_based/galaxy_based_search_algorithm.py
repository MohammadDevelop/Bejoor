import random
import numpy as np
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class GalaxyBasedSearchAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, gravity_constant=0.01, **kwargs):
        """
        Galaxy-based Search Algorithm (GbSA).
        :param gravity_constant: Constant that controls the gravitational pull.
        """
        super().__init__(*args, **kwargs)
        self.gravity_constant = gravity_constant
        self.optimizer_name = "Galaxy-based Search Algorithm"

    def calculate_center_of_mass(self):
        """Calculate the center of mass of the population."""
        total_mass = sum([ind.get_objective_value() for ind in self.population])
        center_of_mass = np.sum([np.array(ind.get_values()) * ind.get_objective_value() for ind in self.population], axis=0)
        return center_of_mass / total_mass

    def update(self):
        """Update the population using galaxy-like attraction toward the center of mass."""
        center_of_mass = self.calculate_center_of_mass()

        new_population = []

        for ind in self.population:
            force = self.gravity_constant * (center_of_mass - np.array(ind.get_values()))
            new_values = np.array(ind.get_values()) + random.random() * force
            new_values = np.clip(new_values, [var['lower_bound'] for var in self.solution_vector], [var['upper_bound'] for var in self.solution_vector])

            new_individual = Individual(ind.id, new_values.tolist())
            new_population.append(new_individual)

        # Evaluate and sort the population
        self.population = new_population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update the best solution
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        # Update global best if necessary
        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
