import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual


class ExchangeMarketAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, trading_probability=0.8, **kwargs):
        """
        Exchange Market Algorithm (EMA) inspired by currency exchange dynamics.

        :param trading_probability: Probability of trading information between individuals (solutions).
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Exchange Market Algorithm"
        self.trading_probability = trading_probability

    def trade(self, buyer, seller):
        """Trade information between two individuals (buyer and seller) to generate new solutions."""
        new_solution = []
        for i in range(self.solution_vector_size):
            if random.random() < self.trading_probability:
                # Buyer takes value from seller with some randomness
                new_value = seller.values[i] + random.uniform(-1, 1) * (seller.values[i] - buyer.values[i])

                # Ensure new value stays within the variable bounds
                if self.solution_vector[i]['type'] == 'integer':
                    new_value = int(max(self.solution_vector[i]['lower_bound'],
                                        min(self.solution_vector[i]['upper_bound'], new_value)))
                elif self.solution_vector[i]['type'] == 'float':
                    new_value = max(self.solution_vector[i]['lower_bound'],
                                    min(self.solution_vector[i]['upper_bound'], new_value))
                new_solution.append(new_value)
            else:
                # Buyer keeps its own value
                new_solution.append(buyer.values[i])
        return new_solution

    def update(self):
        """Update population by allowing individuals to trade information."""
        new_population = []
        self.sort_individuals()  # Sort population by objective value (fitness)

        # Trading phase
        for i in range(0, len(self.population), 2):
            # Select buyer and seller
            buyer = self.population[i]
            seller = self.population[i + 1] if i + 1 < len(self.population) else self.population[0]

            # Buyer trades with seller to generate new solution
            new_solution_values = self.trade(buyer, seller)
            new_individual = Individual(len(new_population), new_solution_values)
            self.evaluate_objective(new_individual)
            new_population.append(new_individual)

        # Update population with new solutions
        self.population = new_population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update best and global best solutions
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value

