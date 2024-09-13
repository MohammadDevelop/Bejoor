import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual
import math

class CuckooSearch(BejoorAlgorithm):
    def __init__(self, *args, pa=0.25, **kwargs):
        """
        Cuckoo Search Algorithm.
        :param pa: Discovery rate of alien eggs/solutions.
        """
        super().__init__(*args, **kwargs)
        self.pa = pa
        self.optimizer_name = "Cuckoo Search"

    def levy_flight(self, step_size=1):
        """Perform Levy flight to generate new solutions."""
        beta = 1.5
        sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        u = random.gauss(0, sigma)
        v = random.gauss(0, 1)
        step = u / (abs(v) ** (1 / beta))
        return step * step_size

    def update(self):
        """Update the population using cuckoo search strategy."""
        new_population = []
        for individual in self.population:
            new_values = [value + self.levy_flight() for value in individual.values]
            new_values = [min(max(new_values[i], self.solution_vector[i]['lower_bound']), self.solution_vector[i]['upper_bound'])
                          for i in range(self.solution_vector_size)]
            new_individual = Individual(individual.id, new_values)
            new_population.append(new_individual)

        # Apply abandonment (pa) for a fraction of the worst solutions
        abandon_count = int(self.pa * self.population_size)
        new_population = sorted(new_population, key=lambda ind: ind.get_objective_value())[:self.population_size - abandon_count]

        # Generate random solutions for the abandoned ones
        while len(new_population) < self.population_size:
            random_values = [random.uniform(self.solution_vector[i]['lower_bound'], self.solution_vector[i]['upper_bound'])
                             for i in range(self.solution_vector_size)]
            new_individual = Individual(len(new_population), random_values)
            new_population.append(new_individual)

        self.population = new_population
        self.evaluate_all_objectives()
        self.sort_individuals()
