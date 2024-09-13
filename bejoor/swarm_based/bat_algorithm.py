import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual
import math


class BatAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, loudness=0.5, pulse_rate=0.5, min_frequency=0.0, max_frequency=2.0, **kwargs):
        """
        BatAlgorithm: Implementation of the Bat Optimization Algorithm.

        :param loudness: The loudness parameter, controlling local search exploitation.
        :param pulse_rate: The pulse rate, controlling the probability of a bat performing a local search.
        :param min_frequency: Minimum frequency for controlling bat velocities.
        :param max_frequency: Maximum frequency for controlling bat velocities.
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Bat Algorithm"
        self.loudness = loudness
        self.pulse_rate = pulse_rate
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.velocities = [self.initialize_velocity() for _ in
                           range(self.population_size)]  # Initializing velocities for each bat

    def initialize_velocity(self):
        """Initialize random velocity for each dimension of the solution."""
        return [random.uniform(-1, 1) for _ in range(self.solution_vector_size)]

    def move_bats(self, global_best_solution):
        """Move bats based on frequency and velocity updates."""
        for i, individual in enumerate(self.population):
            # Update frequency
            frequency = self.min_frequency + (self.max_frequency - self.min_frequency) * random.random()

            # Update velocity and position
            self.velocities[i] = [
                vel + (individual.values[j] - global_best_solution[j]) * frequency
                for j, vel in enumerate(self.velocities[i])
            ]

            # Update position
            individual.values = [
                val + self.velocities[i][j]
                for j, val in enumerate(individual.values)
            ]

            # Apply local search with some probability (pulse_rate)
            if random.random() > self.pulse_rate:
                individual.values = [
                    val + random.uniform(-1, 1) * self.loudness
                    for val in individual.values
                ]

            # Ensure individual values stay within bounds
            for j in range(self.solution_vector_size):
                if self.solution_vector[j]['type'] == 'integer':
                    individual.values[j] = max(self.solution_vector[j]['lower_bound'],
                                               min(self.solution_vector[j]['upper_bound'], int(individual.values[j])))
                elif self.solution_vector[j]['type'] == 'float':
                    individual.values[j] = max(self.solution_vector[j]['lower_bound'],
                                               min(self.solution_vector[j]['upper_bound'], individual.values[j]))

    def update_loudness_and_pulse_rate(self, individual):
        """Update loudness and pulse rate for a bat."""
        # Typically, loudness decreases and pulse rate increases
        self.loudness *= 0.9
        self.pulse_rate = self.pulse_rate * (1 - math.exp(-0.1))

    def update(self):
        """Main update function for the Bat Algorithm."""
        # Move bats
        global_best_solution = self.population[0].values  # Assuming the population is already sorted
        self.move_bats(global_best_solution)

        # Evaluate and sort the population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update loudness and pulse rate for the best bat
        self.update_loudness_and_pulse_rate(self.population[0])

        # Update the best solution
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        # Update the global best solution
        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side =='max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value

