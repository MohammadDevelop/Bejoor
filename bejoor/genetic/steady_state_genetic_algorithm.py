from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.genetic import BaseGeneticAlgorithm
from bejoor.core.individual import Individual
import random


class SteadyStateGeneticAlgorithm(BaseGeneticAlgorithm):
    def __init__(self, *args, offspring_size=2, **kwargs):
        super().__init__(*args, **kwargs)
        self.offspring_size = offspring_size  # Number of offspring generated per generation

    def update(self):
        """Update mechanism for steady-state GA."""
        new_population = self.population[:]

        for _ in range(self.offspring_size):
            parent1, parent2 = self.select_parents()
            child1_values, child2_values = self.crossover(parent1, parent2)

            child1 = Individual(len(new_population), child1_values)
            child2 = Individual(len(new_population) + 1, child2_values)

            self.mutate(child1)
            self.mutate(child2)

            # Add offspring to the population
            new_population.extend([child1, child2])

        # Sort and remove the least fit individuals
        self.population = sorted(new_population, key=lambda ind: ind.get_objective_value() or float('inf'))[
                          :self.population_size]

        self.evaluate_all_objectives()
        self.sort_individuals()

        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
