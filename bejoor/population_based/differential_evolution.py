import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual


class DifferentialEvolution(BejoorAlgorithm):
    def __init__(self, *args, F=0.5, CR=0.7, **kwargs):
        """
        Differential Evolution: Full-featured implementation of the Differential Evolution algorithm.

        :param F: Scaling factor for mutation (0 < F < 2).
        :param CR: Crossover probability (0 <= CR <= 1).
        """
        super().__init__(*args, **kwargs)
        self.optimizer_name = "Differential Evolution"
        self.F = F
        self.CR = CR

    def mutate(self, target, base, diff1, diff2):
        """Mutation operation: base + F * (diff1 - diff2)."""
        mutant_values = []
        for i in range(self.solution_vector_size):
            if self.solution_vector[i]['type'] == 'integer':
                new_value = int(base.get_values()[i] + self.F * (diff1.get_values()[i] - diff2.get_values()[i]))
                new_value = min(max(new_value, self.solution_vector[i]['lower_bound']),
                                self.solution_vector[i]['upper_bound'])
            elif self.solution_vector[i]['type'] == 'float':
                new_value = base.get_values()[i] + self.F * (diff1.get_values()[i] - diff2.get_values()[i])
                new_value = min(max(new_value, self.solution_vector[i]['lower_bound']),
                                self.solution_vector[i]['upper_bound'])
            else:
                new_value = target.get_values()[i]  # For binary/string, don't mutate
            mutant_values.append(new_value)

        return mutant_values

    def crossover(self, target, mutant):
        """Crossover between the target and mutant vectors."""
        trial_values = []
        for i in range(self.solution_vector_size):
            if random.random() < self.CR:
                trial_values.append(mutant[i])
            else:
                trial_values.append(target.get_values()[i])
        return trial_values

    def select_individuals(self):
        """Randomly select three distinct individuals for mutation."""
        candidates = random.sample(self.population, 3)
        return candidates[0], candidates[1], candidates[2]

    def update(self):
        """Main update mechanism for Differential Evolution."""
        new_population = []

        for target in self.population:
            base, diff1, diff2 = self.select_individuals()

            mutant_values = self.mutate(target, base, diff1, diff2)
            trial_values = self.crossover(target, mutant_values)

            # Create a new trial individual
            trial = Individual(target.id, trial_values)

            # Compare trial with the target and select the better one
            trial_objective_value = self.evaluate_objective(trial)
            target_objective_value = self.evaluate_objective(target)

            if (self.optimization_side == 'min' and trial_objective_value < target_objective_value) or \
                    (self.optimization_side == 'max' and trial_objective_value > target_objective_value):
                new_population.append(trial)
            else:
                new_population.append(target)

        # Update the population
        self.population = new_population

        # Re-evaluate objectives and sort the population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update best and global best solutions
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        if ((self.global_best_objective_value is None) or
                (self.optimization_side == 'max' and self.best_objective_value > self.global_best_objective_value) or
                (self.optimization_side == 'min' and self.best_objective_value < self.global_best_objective_value)):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value

