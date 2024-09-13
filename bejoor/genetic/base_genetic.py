from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual
import random


class BaseGeneticAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, crossover_probability=0.9, mutation_probability=0.1, elitism_rate=0.05,
                 selection_strategy="tournament", crossover_type="one-point", **kwargs):
        """
        BaseGeneticAlgorithm: Full-featured implementation of a Genetic Algorithm.

        :param crossover_probability: Probability of crossover.
        :param mutation_probability: Probability of mutation.
        :param elitism_rate: Percentage of the best individuals to preserve.
        :param selection_strategy: Strategy for parent selection (e.g., 'tournament', 'roulette').
        :param crossover_type: Type of crossover ('one-point', 'two-point', 'uniform').
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Base Genetic"
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism_rate = elitism_rate
        self.selection_strategy = selection_strategy
        self.crossover_type = crossover_type

    def select_parents(self):
        """Select two parents based on the selection strategy."""
        if self.selection_strategy == "tournament":
            return self.tournament_selection(), self.tournament_selection()
        elif self.selection_strategy == "roulette":
            return self.roulette_wheel_selection(), self.roulette_wheel_selection()
        else:
            raise ValueError(f"Unsupported selection strategy: {self.selection_strategy}")

    def tournament_selection(self, k=3):
        """Tournament selection mechanism."""
        tournament = random.sample(self.population, k)
        return min(tournament, key=lambda ind: ind.get_objective_value()) if self.optimization_side == 'min' else max(
            tournament, key=lambda ind: ind.get_objective_value())

    def roulette_wheel_selection(self):
        """Roulette-wheel selection based on fitness."""
        fitness_scores = [ind.get_objective_value() for ind in self.population]
        # Normalize the fitness values
        total_fitness = sum(fitness_scores)
        selection_probs = [f / total_fitness for f in fitness_scores]
        return random.choices(self.population, weights=selection_probs, k=1)[0]

    def crossover(self, parent1, parent2):
        """Apply crossover based on the selected crossover type."""
        if random.random() > self.crossover_probability:
            return parent1.values[:], parent2.values[:]

        if self.crossover_type == "one-point":
            point = random.randint(1, self.solution_vector_size - 1)
            child1 = parent1.values[:point] + parent2.values[point:]
            child2 = parent2.values[:point] + parent1.values[point:]
        elif self.crossover_type == "two-point":
            point1 = random.randint(1, self.solution_vector_size - 2)
            point2 = random.randint(point1, self.solution_vector_size - 1)
            child1 = parent1.values[:point1] + parent2.values[point1:point2] + parent1.values[point2:]
            child2 = parent2.values[:point1] + parent1.values[point1:point2] + parent2.values[point2:]
        elif self.crossover_type == "uniform":
            child1, child2 = [], []
            for p1_val, p2_val in zip(parent1.values, parent2.values):
                if random.random() < 0.5:
                    child1.append(p1_val)
                    child2.append(p2_val)
                else:
                    child1.append(p2_val)
                    child2.append(p1_val)
        else:
            raise ValueError(f"Unsupported crossover type: {self.crossover_type}")

        return child1, child2

    def mutate(self, individual):
        """Apply mutation to an individual."""
        for i in range(self.solution_vector_size):
            if random.random() < self.mutation_probability:
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

    def update(self):
        """Update mechanism including elitism, crossover, and mutation."""
        # Preserve the top individuals (elitism)
        elite_count = int(self.elitism_rate * self.population_size)
        elites = self.population[:elite_count]

        new_population = elites[:]

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child1_values, child2_values = self.crossover(parent1, parent2)

            child1 = Individual(len(self.population) + len(new_population), child1_values)
            child2 = Individual(len(self.population) + len(new_population) + 1, child2_values)

            self.mutate(child1)
            self.mutate(child2)

            new_population.extend([child1, child2])

        # Update the population with elites and new individuals
        self.population = new_population

        # Re-evaluate objectives and sort the population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update the best solution
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        # Update the global best solution
        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side =='max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
