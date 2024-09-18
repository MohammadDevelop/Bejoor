import random
import numpy as np
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual


class BarnaclesMatingOptimizer(BejoorAlgorithm):
    def __init__(self, *args, mating_rate=0.8, growth_rate=0.1, **kwargs):
        """
        Barnacles Mating Optimizer (BMO) implementation.

        :param mating_rate: Probability of mating (controls exploitation).
        :param growth_rate: Rate of growth (controls exploration).
        """
        super().__init__(*args, **kwargs)
        self.mating_rate = mating_rate
        self.growth_rate = growth_rate
        self.optimizer_name = "Barnacles Mating Optimizer"

    def mate(self, barnacle1, barnacle2):
        """Mate two barnacles (solutions) to produce offspring."""
        new_values = []
        for i in range(self.solution_vector_size):
            if random.random() < 0.5:
                new_value = barnacle1.values[i]
            else:
                new_value = barnacle2.values[i]

            # Small random growth mutation
            new_value += self.growth_rate * np.random.uniform(-1, 1) * (
                        self.solution_vector[i]['upper_bound'] - self.solution_vector[i]['lower_bound'])

            # Ensure new value is within bounds
            new_value = np.clip(new_value, self.solution_vector[i]['lower_bound'],
                                self.solution_vector[i]['upper_bound'])
            new_values.append(new_value)

        return new_values

    def update(self):
        """Update population using the Barnacles Mating Optimizer."""
        new_population = []

        # Sort the population to select the best individuals for mating
        self.sort_individuals()

        # Select top individuals for mating
        elite_count = int(self.mating_rate * self.population_size)
        elites = self.population[:elite_count]

        # Mate elites to create new offspring
        for _ in range(self.population_size):
            parent1, parent2 = random.sample(elites, 2)
            offspring_values = self.mate(parent1, parent2)

            new_individual = Individual(len(self.population) + len(new_population), offspring_values)
            new_population.append(new_individual)

        # Update population with new individuals
        self.population = new_population

        # Evaluate objectives for the new population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update the best solution
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        # Update the global best solution if necessary
        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value

    def run(self):
        """Run the Barnacles Mating Optimizer."""
        self.current_iteration = 0  # Reset iteration tracker
        super().run()  # Run the base algorithm setup
        for epoch_index in range(1, self.epochs + 1):
            self.current_iteration = epoch_index
            self.update()

            # Log progress
            print(f'{self.optimizer_name} (pop:{len(self.population)}) |'
                  f' Epoch #{epoch_index}: Current best:{self.best_objective_value}'
                  f' Global best:{self.global_best_objective_value}')

            if self.target_objective_value is not None and self.best_objective_value == self.target_objective_value:
                print(f"Target Objective Value ({self.best_objective_value}) reached before end of all iterations.")
                break

            if self.target_objective_lower_bound is not None and self.best_objective_value >= self.target_objective_lower_bound:
                print(
                    f"Target Objective lower bound ({self.best_objective_value}) reached before end of all iterations.")
                break

            if self.target_objective_upper_bound is not None and self.best_objective_value <= self.target_objective_upper_bound:
                print(
                    f"Target Objective upper bound ({self.best_objective_value}) reached before end of all iterations.")
                break
