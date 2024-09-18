from bejoor.genetic import BaseGeneticAlgorithm
from bejoor.core import Individual
def sphere_function(sol):
    return sum(x**2 for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

ga = BaseGeneticAlgorithm(objective_function=sphere_function, solution_vector_size=7,
                          solution_vector=solution_vector, optimization_side="min",
                          population_size=300, epochs=50)

self_defined_values=[
    [-5, -4, -3, 0, 2, 3, 4],
    [-1, 1, -1, 1, -1, 1, -1],
    [1, 0, 0, 0, 1, 0, 0],
    [2, 4, 3, 0, 2, 3, 4],
    [-0.5, -0.4, -0.3, 0, 0.2, 0.3, 0.4],
    [-0.1, -0.1, -0.1, 0, 0.1, 0.1, 0.1],
]

individuals = []

for index, vector in enumerate(self_defined_values):
    individual = Individual(index, vector)
    individuals.append(individual)

ga.run(init_population=individuals)

print(f'Best Global Objective Value: {ga.global_best_objective_value}')
print(f'Best Global Solution: {ga.global_best_solution}')
