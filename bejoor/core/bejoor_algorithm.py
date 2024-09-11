import random
from bejoor.core.individual import Individual

class BejoorAlgorithm:
    def __init__(self, objective_function, solution_vector_size, solution_vector, optimization_side , population_size=10, epochs=5):
        """
        Initialize the base parameters for the optimization algorithm.

        :param objective_function: Objective function needs to be optimized.
        :param solution_vector_size: Vector size of the candidate solutions.
        :param solution_vector: A vector which determines the types of each variable in solution vectors.
        :param optimization_side: Determines maximize or minimize the objective function.
        :param population_size: Number of individuals in the population
        :param epochs: Number of generations to run the algorithm
        """

        if not isinstance(solution_vector, list):
            raise TypeError("The 'types' parameter must be a list.")
        if len(solution_vector) != solution_vector_size:
            raise ValueError(f"The 'types' list must have exactly {solution_vector_size} elements.")

        self.population_size = population_size
        self.epochs = epochs
        self.objective_function = objective_function
        self.solution_vector_size = solution_vector_size
        self.optimization_side = optimization_side
        self.solution_vector = solution_vector
        self.population = []
        self.best_objective_value = None
        self.best_solution = None

    def initialize_population(self):
        """Initialize the population for the evolutionary algorithm."""
        self.population = []
        for index in range(self.population_size):
            individual_values = []
            for i in range(self.solution_vector_size):
                if self.solution_vector[i]['type'] == 'string':
                    individual_values.append(random.choice(self.solution_vector[i]['possible_values']))
                elif self.solution_vector[i]['type'] == 'binary':
                    individual_values.append(random.choice([True, False]))
                elif self.solution_vector[i]['type'] == 'integer':
                    individual_values.append(
                        random.randint(self.solution_vector[i]['lower_bound'], self.solution_vector[i]['upper_bound']))
                elif self.solution_vector[i]['type'] == 'float':
                    individual_values.append(
                        random.uniform(self.solution_vector[i]['lower_bound'], self.solution_vector[i]['upper_bound']))
                else:
                    raise ValueError(f"Unsupported type '{self.solution_vector[i]}' at index {i}")

            # Create an individual and append to the population
            individual = Individual(index, individual_values)
            self.population.append(individual)

    def evaluate_objective(self, individual):
        """Evaluate the objective of an individual."""
        objective_value = self.objective_function(individual.get_values())
        individual.set_objective_value(objective_value)
        return objective_value

    def evaluate_all_objectives(self):
        for individual in self.population:
            objective_value = self.objective_function(individual.get_values())
            individual.set_objective_value(objective_value)
        pass

    def sort_individuals(self):
        """Sort the population according to the optimization side ('min' or 'max')."""
        if self.optimization_side == 'min':
            self.population.sort(key=lambda ind: ind.get_objective_value())
        elif self.optimization_side == 'max':
            self.population.sort(key=lambda ind: ind.get_objective_value(), reverse=True)
        else:
            raise ValueError("optimization_side must be 'min' or 'max'")

    def update(self):
        """Perform update mechanism of the algorithm."""
        # This is the main part of implementing different algorithms
        # This implementation here is just adding random individuals
        for index in range(3):
            individual_values = []
            for i in range(self.solution_vector_size):
                if self.solution_vector[i]['type'] == 'string':
                    individual_values.append(random.choice(self.solution_vector[i]['possible_values']))
                elif self.solution_vector[i]['type'] == 'binary':
                    individual_values.append(random.choice([True, False]))
                elif self.solution_vector[i]['type'] == 'integer':
                    individual_values.append(
                        random.randint(self.solution_vector[i]['lower_bound'],
                                        self.solution_vector[i]['upper_bound']))
                elif self.solution_vector[i]['type'] == 'float':
                    individual_values.append(
                        random.uniform(self.solution_vector[i]['lower_bound'],
                                        self.solution_vector[i]['upper_bound']))
                else:
                    raise ValueError(f"Unsupported type '{self.solution_vector[i]}' at index {i}")

                # Create an individual and append to the population
            individual = Individual(index, individual_values)
            self.population.append(individual)

        self.evaluate_all_objectives()
        self.sort_individuals()
        self.population=self.population[:self.population_size]

        pass

    def run(self):
        """Run the algorithm."""
        self.initialize_population()
        self.evaluate_all_objectives()

        print(len(self.population))
        for epoch_index in range(1,self.epochs):
            self.update()

            self.best_solution = self.population[0].values
            self.best_objective_value = self.population[0].objective_value

            print(f'Epoch #{epoch_index}: best:{self.best_objective_value} - {len(self.population)}')

