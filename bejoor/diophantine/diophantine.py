import math
from bejoor.core.individual import Individual

def evaluate(eq, solution, solution_set='int'):
    left = eq.split("=")[0]
    right = float(eq.split("=")[1])  # Convert the right-hand side to float for numerical operations
    eq_str = left
    if solution_set == 'int':
        for i in range(len(solution), 0, -1):
            eq_str = eq_str.replace("x" + str(i), str(math.floor(solution[i - 1])))
    else:
        for i in range(len(solution), 0, -1):
            eq_str = eq_str.replace("x" + str(i), str(solution[i - 1]))
    return (right - eval(eq_str)) ** 2

class DiophantineEquation:
    def __init__(self, equation_system, num_variables, lower_bound, upper_bound, target_solution_set='int'):
        """
        :param equation_system: List of equations to be solved
        :param num_variables: Number of variables in the system
        :param lower_bound: List of Lower bounds of variables in the system
        :param upper_bound: List of Upper bounds of variables in the system
        :param target_solution_set: Solution set type (e.g., 'int' or 'float')
        """
        self.equation_system = equation_system
        self.num_variables = num_variables
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.target_solution_set = target_solution_set

    def fitness(self, solution):
        """
        Calculate fitness based on the sum of squared differences from the target solutions.
        """
        total_fitness = 0
        for eq in self.equation_system:
            total_fitness += evaluate(eq, solution, solution_set=self.target_solution_set)
        return total_fitness

    def solve(self, optimizer_class, population_size=50, epochs=100):
        """
        Solve the system of Diophantine equations using a given optimizer.
        :param optimizer_class: Optimization algorithm class (e.g., BaseGeneticAlgorithm)
        :param population_size: Population size for the optimizer
        :param epochs: Number of iterations for the optimizer
        :return: Best solution found by the optimizer
        """
        # Define the objective function based on fitness
        def objective_function(solution):
            return self.fitness(solution)

        # Define the solution vector (either integer or float based on the solution set)
        solution_vector = [
            {'type': 'integer', 'lower_bound': self.lower_bound[i], 'upper_bound': self.upper_bound[i]} if self.target_solution_set == 'int'
            else {'type': 'float', 'lower_bound': self.lower_bound[i], 'upper_bound': self.upper_bound[i]}
            for i in range(self.num_variables)
        ]

        # Initialize and run the optimizer
        optimizer = optimizer_class(
            objective_function=objective_function,
            solution_vector_size=self.num_variables,
            solution_vector=solution_vector,
            optimization_side='min',  # We want to minimize the fitness (i.e., error)
            population_size=population_size,
            epochs=epochs
        )
        optimizer.run()

        # Return the best solution found
        return optimizer.global_best_solution, optimizer.global_best_objective_value

