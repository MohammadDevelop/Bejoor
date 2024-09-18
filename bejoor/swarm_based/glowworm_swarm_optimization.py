import random
import numpy as np
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class GlowwormSwarmOptimization(BejoorAlgorithm):
    def __init__(self, *args, luciferin_decay=0.4, luciferin_enhancement=0.6, sensing_range=3.0, neighbor_count=5,
                 step_size=0.03, **kwargs):
        """
        Glowworm Swarm Optimization (GSO) implementation.

        :param luciferin_decay: Decay rate of luciferin (light intensity).
        :param luciferin_enhancement: Enhancement rate of luciferin after objective evaluation.
        :param sensing_range: The radius within which glowworms sense each other.
        :param neighbor_count: Maximum number of neighbors a glowworm can consider.
        :param step_size: The step size used to move towards neighbors.
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Glowworm Swarm Optimization"
        self.luciferin_decay = luciferin_decay
        self.luciferin_enhancement = luciferin_enhancement
        self.sensing_range = sensing_range
        self.neighbor_count = neighbor_count
        self.step_size = step_size

        # Initialize luciferin values (light intensity) for each individual in the population
        self.luciferin = [random.random() for _ in range(self.population_size)]

    def update_luciferin(self):
        """Update the luciferin values for each glowworm based on their objective values."""
        for i, individual in enumerate(self.population):
            objective_value = individual.get_objective_value()
            # Decay and enhance luciferin based on objective value
            self.luciferin[i] = (1 - self.luciferin_decay) * self.luciferin[i] + self.luciferin_enhancement * objective_value

    def find_neighbors(self, glowworm_idx):
        """Find the neighbors of a glowworm within its sensing range."""
        neighbors = []
        current_glowworm = self.population[glowworm_idx]

        for idx, glowworm in enumerate(self.population):
            if idx != glowworm_idx:
                distance = np.linalg.norm(np.array(current_glowworm.values) - np.array(glowworm.values))
                if distance <= self.sensing_range and self.luciferin[glowworm_idx] < self.luciferin[idx]:
                    neighbors.append(idx)

        # Limit neighbors to the max neighbor count
        if len(neighbors) > self.neighbor_count:
            neighbors = random.sample(neighbors, self.neighbor_count)

        return neighbors

    def move_glowworm(self, glowworm_idx, neighbor_idx):
        """Move a glowworm towards its chosen neighbor."""
        current_position = np.array(self.population[glowworm_idx].values)
        neighbor_position = np.array(self.population[neighbor_idx].values)
        direction = neighbor_position - current_position

        # Normalize the direction and move a step towards the neighbor
        if np.linalg.norm(direction) != 0:
            direction = direction / np.linalg.norm(direction)
        new_position = current_position + self.step_size * direction

        # Ensure new position stays within bounds
        for i in range(self.solution_vector_size):
            new_position[i] = np.clip(new_position[i], self.solution_vector[i]['lower_bound'], self.solution_vector[i]['upper_bound'])

        return new_position.tolist()

    def update(self):
        """Update the population of glowworms based on the GSO algorithm."""
        self.update_luciferin()

        new_population = []

        for i, glowworm in enumerate(self.population):
            neighbors = self.find_neighbors(i)

            if neighbors:
                chosen_neighbor = random.choice(neighbors)
                new_values = self.move_glowworm(i, chosen_neighbor)

                new_individual = Individual(i, new_values)
                new_population.append(new_individual)
            else:
                new_population.append(glowworm)

        # Update population with the new positions
        self.population = new_population

        # Evaluate objectives for the new population
        self.evaluate_all_objectives()

        # Update the best solution found so far
        self.sort_individuals()
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        # Update the global best solution if necessary
        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
