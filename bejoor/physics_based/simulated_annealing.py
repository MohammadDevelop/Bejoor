import random
import math
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual


class SimulatedAnnealing(BejoorAlgorithm):
    def __init__(self, *args, initial_temperature=1000, cooling_rate=0.9, **kwargs):
        """
        SimulatedAnnealing: Full-featured implementation of Simulated Annealing algorithm.

        :param initial_temperature: The starting temperature for the annealing process.
        :param cooling_rate: The rate at which the temperature decreases.
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Simulated Annealing"
        self.initial_temperature = initial_temperature
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate

    def mutate(self, individual):
        """Small random modification to the individual's solution vector."""
        mutated_values = individual.get_values()[:]
        i = random.randint(0, self.solution_vector_size - 1)

        if self.solution_vector[i]['type'] == 'binary':
            mutated_values[i] = not mutated_values[i]
        elif self.solution_vector[i]['type'] == 'integer':
            mutated_values[i] = random.randint(
                self.solution_vector[i]['lower_bound'],
                self.solution_vector[i]['upper_bound']
            )
        elif self.solution_vector[i]['type'] == 'float':
            mutated_values[i] = random.uniform(
                self.solution_vector[i]['lower_bound'],
                self.solution_vector[i]['upper_bound']
            )

        return Individual(individual.id, mutated_values)

    def accept_solution(self, old_value, new_value):
        """Decide whether to accept the new solution."""
        if self.optimization_side == 'min':
            delta = new_value - old_value
        else:
            delta = old_value - new_value

        if delta < 0:
            return True
        else:
            return math.exp(-delta / self.temperature) > random.random()

    def update(self):
        """Main update mechanism for Simulated Annealing."""
        current_solution = self.population[0]
        current_value = self.evaluate_objective(current_solution)

        new_solution = self.mutate(current_solution)
        new_value = self.evaluate_objective(new_solution)

        if self.accept_solution(current_value, new_value):
            self.population[0] = new_solution
            current_value = new_value

        # Cool down the temperature
        self.temperature *= self.cooling_rate

        # Update best and global best solutions
        self.best_solution = self.population[0].values
        self.best_objective_value = current_value

        if ((self.global_best_objective_value is None) or
                (self.optimization_side == 'max' and current_value > self.global_best_objective_value) or
                (self.optimization_side == 'min' and current_value < self.global_best_objective_value)):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = current_value

    def run(self):
        """Run the Simulated Annealing algorithm."""
        self.initialize_population()
        self.evaluate_all_objectives()

        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value
        self.global_best_solution = self.best_solution
        self.global_best_objective_value = self.best_objective_value

        for epoch_index in range(1, self.epochs):
            self.update()

            print(f'{self.optimizer_name} (temp: {self.temperature}) | Epoch #{epoch_index}: '
                  f'Current best:{self.best_objective_value} Global best:{self.global_best_objective_value}')

            if self.temperature < 1e-3:  # Stop if temperature is too low
                print("Temperature too low, stopping.")
                break
