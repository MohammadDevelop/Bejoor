import random
import numpy as np
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class WhaleOptimizationAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, a_max=2.0, a_min=0.0, **kwargs):
        """
        Whale Optimization Algorithm (WOA).
        :param a_max: Maximum value of the control parameter 'a' (controls exploration).
        :param a_min: Minimum value of the control parameter 'a' (controls exploitation).
        """
        super().__init__(*args, **kwargs)
        self.a_max = a_max
        self.a_min = a_min
        self.optimizer_name = "Whale Optimization Algorithm"

    def update(self):
        """Update population using the Whale Optimization Algorithm."""
        a = self.a_max - (self.a_max - self.a_min) * (self.current_iteration / self.epochs)

        new_population = []

        for ind in self.population:
            new_values = []

            for i, value in enumerate(ind.get_values()):
                r1 = random.random()  # Random number between 0 and 1
                r2 = random.random()  # Random number between 0 and 1

                if r1 < 0.5:
                    # Encircling prey
                    C = 2 * r2
                    D = abs(C * self.global_best_solution[i] - value)
                    new_value = self.global_best_solution[i] - a * D
                else:
                    # Bubble-net attacking method
                    p = random.random()
                    if p < 0.5:
                        # Spiral update
                        D = abs(self.global_best_solution[i] - value)
                        new_value = D * np.exp(2 * np.pi * r2) * np.cos(2 * np.pi * r2) + self.global_best_solution[i]
                    else:
                        # Random search
                        new_value = self.global_best_solution[i] + np.random.uniform(-1, 1) * (self.global_best_solution[i] - value)

                # Ensure new value is within bounds
                new_value = np.clip(new_value, self.solution_vector[i]['lower_bound'], self.solution_vector[i]['upper_bound'])
                new_values.append(new_value)

            # Create new individual
            new_individual = Individual(ind.id, new_values)
            new_population.append(new_individual)

        # Update population and evaluate
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

    def run(self):
        """Run the Whale Optimization Algorithm."""
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
                print(f"Target Objective lower bound ({self.best_objective_value}) reached before end of all iterations.")
                break

            if self.target_objective_upper_bound is not None and self.best_objective_value <= self.target_objective_upper_bound:
                print(f"Target Objective upper bound ({self.best_objective_value}) reached before end of all iterations.")
                break
