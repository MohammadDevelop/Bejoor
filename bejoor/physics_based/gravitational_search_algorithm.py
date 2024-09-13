import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual
import math

class GravitationalSearchAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, G_initial=100, G_decay=0.99, **kwargs):
        """
        Gravitational Search Algorithm (GSA).
        :param G_initial: Initial value of gravitational constant.
        :param G_decay: Decay rate of gravitational constant per iteration.
        """
        super().__init__(*args, **kwargs)
        self.G = G_initial
        self.G_decay = G_decay
        self.optimizer_name = "Gravitational Search Algorithm"

    def calculate_mass(self):
        """Calculate the mass of each individual based on its fitness."""
        fitness_values = [ind.get_objective_value() for ind in self.population]
        worst = max(fitness_values) if self.optimization_side == 'min' else min(fitness_values)
        best = min(fitness_values) if self.optimization_side == 'min' else max(fitness_values)

        masses = []
        for fitness in fitness_values:
            if best == worst:
                masses.append(1.0)
            else:
                mass = (fitness - worst) / (best - worst)
                masses.append(mass)
        total_mass = sum(masses)
        return [mass / total_mass for mass in masses]

    def update(self):
        """Update positions and velocities based on gravitational force."""
        masses = self.calculate_mass()
        new_population = []

        for i, individual in enumerate(self.population):
            force = [0] * self.solution_vector_size
            for j, other_ind in enumerate(self.population):
                if i != j:
                    distance = math.sqrt(sum((individual.values[k] - other_ind.values[k]) ** 2 for k in range(self.solution_vector_size)))
                    for k in range(self.solution_vector_size):
                        force[k] += random.random() * self.G * masses[j] * (other_ind.values[k] - individual.values[k]) / (distance + 1e-10)

            # Update positions based on force
            new_values = []
            for k in range(self.solution_vector_size):
                new_value = individual.values[k] + force[k]
                new_value = min(max(new_value, self.solution_vector[k]['lower_bound']), self.solution_vector[k]['upper_bound'])
                new_values.append(new_value)

            new_individual = Individual(individual.id, new_values)
            new_population.append(new_individual)

        # Update the population
        self.population = new_population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Decay the gravitational constant
        self.G *= self.G_decay
