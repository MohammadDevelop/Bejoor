import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class HarmonySearch(BejoorAlgorithm):
    def __init__(self, *args, HMCR=0.9, PAR=0.3, **kwargs):
        """
        Harmony Search algorithm.
        :param HMCR: Harmony memory consideration rate (probability of choosing values from the harmony memory).
        :param PAR: Pitch adjustment rate (probability of fine-tuning a selected value).
        """
        super().__init__(*args, **kwargs)
        self.HMCR = HMCR
        self.PAR = PAR
        self.optimizer_name = "Harmony Search"

    def improvise(self):
        """Create a new harmony (solution) by considering the harmony memory."""
        new_values = []
        for i in range(self.solution_vector_size):
            if random.random() < self.HMCR:  # Choose from memory
                value = random.choice([ind.values[i] for ind in self.population])
                if random.random() < self.PAR:  # Apply pitch adjustment
                    if self.solution_vector[i]['type'] == 'integer':
                        value += random.choice([-1, 1])
                        value = min(max(value, self.solution_vector[i]['lower_bound']),
                                    self.solution_vector[i]['upper_bound'])
                    elif self.solution_vector[i]['type'] == 'float':
                        value += random.uniform(-0.1, 0.1)
                        value = min(max(value, self.solution_vector[i]['lower_bound']),
                                    self.solution_vector[i]['upper_bound'])
            else:  # Choose randomly within the allowed range
                if self.solution_vector[i]['type'] == 'integer':
                    value = random.randint(self.solution_vector[i]['lower_bound'], self.solution_vector[i]['upper_bound'])
                elif self.solution_vector[i]['type'] == 'float':
                    value = random.uniform(self.solution_vector[i]['lower_bound'], self.solution_vector[i]['upper_bound'])
            new_values.append(value)
        return new_values

    def update(self):
        """Create new harmonies and update the population."""
        new_population = []
        for _ in range(self.population_size):
            new_values = self.improvise()
            new_individual = Individual(len(self.population) + len(new_population), new_values)
            new_population.append(new_individual)

        # Update population and evaluate new harmonies
        self.population = new_population
        self.evaluate_all_objectives()
        self.sort_individuals()
