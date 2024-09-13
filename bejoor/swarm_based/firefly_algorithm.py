import random
import math
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class FireflyAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, alpha=0.2, beta_0=1.0, gamma=1.0, **kwargs):
        """
        Firefly Algorithm.
        :param alpha: Randomization parameter.
        :param beta_0: Attraction coefficient base value.
        :param gamma: Absorption coefficient.
        """
        super().__init__(*args, **kwargs)
        self.alpha = alpha
        self.beta_0 = beta_0
        self.gamma = gamma
        self.optimizer_name = "Firefly Algorithm"

    def attractiveness(self, distance):
        """Calculate the attractiveness based on the distance."""
        return self.beta_0 * math.exp(-self.gamma * (distance ** 2))

    def update(self):
        """Move fireflies towards brighter ones."""
        for i in range(self.population_size):
            for j in range(self.population_size):
                if self.population[j].get_objective_value() < self.population[i].get_objective_value():
                    distance = math.sqrt(sum((self.population[i].values[k] - self.population[j].values[k]) ** 2
                                             for k in range(self.solution_vector_size)))
                    beta = self.attractiveness(distance)
                    for k in range(self.solution_vector_size):
                        self.population[i].values[k] += beta * (self.population[j].values[k] - self.population[i].values[k]) + \
                                                        self.alpha * (random.uniform(-1, 1))
                        # Ensure within bounds
                        self.population[i].values[k] = min(max(self.population[i].values[k], self.solution_vector[k]['lower_bound']),
                                                           self.solution_vector[k]['upper_bound'])

        self.evaluate_all_objectives()
        self.sort_individuals()
