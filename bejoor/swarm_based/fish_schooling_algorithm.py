import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual


class FishSchoolingAlgorithm(BejoorAlgorithm):
    def __init__(self, *args, visual_range=0.1, step_individual=0.01, step_volitive=0.02, **kwargs):
        """
        Fish Schooling Algorithm (FSA) implementation.

        :param visual_range: Maximum distance for an individual to "see" neighbors.
        :param step_individual: Maximum step size for individual fish movement.
        :param step_volitive: Step size for collective (volitive) movement.
        """
        super().__init__(*args, **kwargs)
        self.visual_range = visual_range
        self.step_individual = step_individual
        self.step_volitive = step_volitive
        self.optimizer_name = "Fish Schooling Algorithm"

    def euclidean_distance(self, pos1, pos2):
        return sum((x1 - x2) ** 2 for x1, x2 in zip(pos1, pos2)) ** 0.5

    def move_individual(self, individual, best_neighbor):
        for i in range(self.solution_vector_size):
            step = random.uniform(-self.step_individual, self.step_individual)
            individual.values[i] += step * (best_neighbor.values[i] - individual.values[i])

    def update(self):
        """Update positions of fish in the school."""
        for individual in self.population:
            # Find the best neighboring fish
            best_neighbor = None
            best_objective_value = float('inf') if self.optimization_side == 'min' else -float('inf')

            for other_individual in self.population:
                if other_individual != individual and self.euclidean_distance(individual.values,
                                                                              other_individual.values) < self.visual_range:
                    objective_value = other_individual.get_objective_value()
                    if (self.optimization_side == 'min' and objective_value < best_objective_value) or \
                            (self.optimization_side == 'max' and objective_value > best_objective_value):
                        best_neighbor = other_individual
                        best_objective_value = objective_value

            if best_neighbor:
                self.move_individual(individual, best_neighbor)

        # Collective volitive movement
        center_of_mass = [sum(ind.values[i] for ind in self.population) / self.population_size for i in
                          range(self.solution_vector_size)]

        for individual in self.population:
            for i in range(self.solution_vector_size):
                step = random.uniform(-self.step_volitive, self.step_volitive)
                individual.values[i] += step * (center_of_mass[i] - individual.values[i])

        # Re-evaluate objectives and sort the population
        self.evaluate_all_objectives()
        self.sort_individuals()

        # Update best and global best
        self.best_solution = self.population[0].values
        self.best_objective_value = self.population[0].objective_value

        if ((self.global_best_objective_value < self.best_objective_value and self.optimization_side == 'max') or
                (self.global_best_objective_value > self.best_objective_value and self.optimization_side == 'min')):
            self.global_best_solution = self.best_solution
            self.global_best_objective_value = self.best_objective_value
