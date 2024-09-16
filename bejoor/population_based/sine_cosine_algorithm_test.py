from bejoor.population_based import SineCosineAlgorithm
import math
def rastrigin_function(sol):
    n = len(sol)
    return 10 * n + sum(x**2 - 10 * math.cos(2 * math.pi * x) for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

csa = SineCosineAlgorithm(objective_function=rastrigin_function, solution_vector_size=7,
                           solution_vector=solution_vector, optimization_side="min",
                           a_max=2.0, a_min=0.0, population_size=30, epochs=50)
csa.run()

print(f'Best Global Objective Value: {csa.global_best_objective_value}')
print(f'Best Global Solution: {csa.global_best_solution}')
