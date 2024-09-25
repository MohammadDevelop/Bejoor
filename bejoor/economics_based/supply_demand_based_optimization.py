import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual


class SupplyDemandOptimization(BejoorAlgorithm):
    def __init__(self, *args, supply_probability=0.5, **kwargs):
        """
        Supply Demand Optimization (SDO) implementation.

        :param supply_probability: Probability of increasing supply to a solution.
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Supply Demand Optimization"
        self.supply_probability = supply_probability

    def update(self):
        """Perform the update process based on supply and demand mechanics."""
        new_population = []

        for individual in self.population:
            new_values = []
            for i in range(self.solution_vector_size):
                if random.random() < self.supply_probability:
                    new_values.append(random.uniform(self.solution_vector[i]['lower_bound'],
                                                     self.solution_vector[i]['upper_bound']))
                else:
                    new_values.append(individual.values[i])

            # Create new individuals
            new_individual = Individual(len(self.population) + len(new_population), new_values)
            new_population.append(new_individual)

        # Evaluate the new population
        self.population = new_population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update best solutions
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
