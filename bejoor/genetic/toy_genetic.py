from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual
import random

class ToyGeneticAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, mutation_probability = 0.15, **kwargs):

        """
        ToyGeneticAlgorithm : toy implementation of GA!

        :param mutation_probability: Mutation Probability
        """

        super().__init__(*args, **kwargs)
        self.mutation_probability = mutation_probability

    def select_parents(self):
        """Select two parents based on rank-based selection."""
        # Calculate total rank
        total_rank = sum(range(1, len(self.population) + 1))

        # Calculate selection probabilities based on rank
        probabilities = [rank / total_rank for rank in range(1, len(self.population) + 1)]

        # Select two parents using the calculated probabilities
        parent1 = random.choices(self.population, weights=probabilities, k=1)[0]
        parent2 = random.choices(self.population, weights=probabilities, k=1)[0]

        return parent1, parent2

    def mutate(self, individual):
        """Apply mutation to an individual based on the mutation probability."""
        if random.random() < self.mutation_probability:
            for i in range(self.solution_vector_size):
                if self.solution_vector[i]['type'] == 'binary':
                    individual.values[i] = not individual.values[i]
                elif self.solution_vector[i]['type'] == 'integer':
                    individual.values[i] = random.randint(
                        self.solution_vector[i]['lower_bound'],
                        self.solution_vector[i]['upper_bound']
                    )
                elif self.solution_vector[i]['type'] == 'float':
                    individual.values[i] = random.uniform(
                        self.solution_vector[i]['lower_bound'],
                        self.solution_vector[i]['upper_bound']
                    )
                # Note: Mutation logic for 'string' type not implemented in this implementation of GA

    def update(self):
        """Custom update mechanism for ToyGeneticAlgorithm."""
        new_population = []

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()

            # Generate offspring by combining parents
            crossover_point = random.randint(1, self.solution_vector_size - 1)
            child1_values = parent1.values[:crossover_point] + parent2.values[crossover_point:]
            child2_values = parent2.values[:crossover_point] + parent1.values[crossover_point:]

            child1 = Individual(len(self.population) + len(new_population), child1_values)
            child2 = Individual(len(self.population) + len(new_population) + 1, child2_values)

            # Apply mutation to the offspring
            self.mutate(child1)
            self.mutate(child2)

            new_population.extend([child1, child2])

        # Concat old and new populations
        self.population = self.population + new_population

        # Re-evaluate and sort the new population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Keep only quantity of population_size in population
        self.population=self.population[:self.population_size]


        # Update the best solution
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value