import random
import numpy as np
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class ElectromagneticFieldOptimization(BejoorAlgorithm):
    def __init__(self, *args, charge_intensity=1, **kwargs):
        """
        Electromagnetic Field Optimization (EFO).
        :param charge_intensity: Intensity of the electrical charge.
        """
        super().__init__(*args, **kwargs)
        self.charge_intensity = charge_intensity
        self.optimizer_name = "Electromagnetic Field Optimization"

    def calculate_charge(self, objective_value):
        """Calculate the charge of an individual based on its objective value."""
        # Normalize fitness
        charge = objective_value * self.charge_intensity
        return charge

    def update(self):
        """Update the population based on electromagnetic attraction/repulsion."""
        new_population = []

        for i in range(self.population_size):
            total_force = np.zeros(self.solution_vector_size)

            for j in range(self.population_size):
                if i != j:
                    charge_i = self.calculate_charge(self.population[i].get_objective_value())
                    charge_j = self.calculate_charge(self.population[j].get_objective_value())
                    distance = np.linalg.norm(np.array(self.population[i].get_values()) - np.array(self.population[j].get_values()))

                    # Attraction or repulsion
                    force_direction = 1 if charge_i * charge_j > 0 else -1
                    force = (charge_i * charge_j) / (distance + 1e-10)
                    total_force += force_direction * force * (np.array(self.population[j].get_values()) - np.array(self.population[i].get_values()))

            # Update individual position
            new_values = np.array(self.population[i].get_values()) + random.random() * total_force
            new_values = np.clip(new_values, [var['lower_bound'] for var in self.solution_vector], [var['upper_bound'] for var in self.solution_vector])

            # Create new individual
            new_individual = Individual(self.population[i].id, new_values.tolist())
            new_population.append(new_individual)

        # Evaluate and sort the population
        self.population = new_population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update best solution
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        # Update global best if necessary
        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
