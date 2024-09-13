from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual
import random
import math

class SalpSwarmAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, c_1, **kwargs):
        """
        SalpSwarmAlgorithm : Implements the SSA.

        :param c_1: Exploration-Exploitation Coefficient (used to balance exploration and exploitation).
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Salp Swarm Algorithm"
        self.leader = None
        self.followers = []
        self.c_1 = c_1
        self.epoch_counter = 0  # Track the current epoch to reduce c_1 over time.

    def update(self):
        """Custom update mechanism for SalpSwarmAlgorithm."""
        new_population = []

        # Update leader salp's position (first individual in the population)
        leader = self.population[0]
        for i in range(self.solution_vector_size):
            F = self.best_solution[i]  # Best solution (food source)
            r1 = random.random()
            r2 = random.random()
            upper_bound = self.solution_vector[i]['upper_bound']
            lower_bound = self.solution_vector[i]['lower_bound']

            if r1 >= 0.5:
                leader.values[i] = F + self.c_1 * (upper_bound - lower_bound) * r2 + lower_bound
            else:
                leader.values[i] = F - self.c_1 * (upper_bound - lower_bound) * r2 + lower_bound

            # Clip values to stay within bounds
            leader.values[i] = min(max(leader.values[i], lower_bound), upper_bound)

        new_population.append(leader)

        # Update the followers (remaining individuals in the population)
        for j in range(1, self.population_size):
            follower = self.population[j]
            for i in range(self.solution_vector_size):
                # Follower update (based on the one ahead)
                follower.values[i] = (self.population[j-1].values[i] + follower.values[i]) / 2

                # Clip values to stay within bounds
                upper_bound = self.solution_vector[i]['upper_bound']
                lower_bound = self.solution_vector[i]['lower_bound']
                follower.values[i] = min(max(follower.values[i], lower_bound), upper_bound)

            new_population.append(follower)

        # Replace the population with the new one
        self.population = new_population

        # Re-evaluate the objective function and sort individuals
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update the best solution if necessary
        if (self.optimization_side == 'min' and self.population[0].objective_value < self.best_objective_value) or \
           (self.optimization_side == 'max' and self.population[0].objective_value > self.best_objective_value):
            self.best_solution = self.population[0].values
            self.best_objective_value = self.population[0].objective_value

        # Update the exploration-exploitation coefficient (c_1) to decrease over time
        self.c_1 = 2 * math.exp(-4 * self.epoch_counter / self.epochs)
        self.epoch_counter += 1

        # Update the global best solution
        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side =='max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
