from bejoor.population_based import HarmonySearch
import math
def rastrigin_function(sol):
    n = len(sol)
    return 10 * n + sum(x**2 - 10 * math.cos(2 * math.pi * x) for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

hs = HarmonySearch(objective_function=rastrigin_function, solution_vector_size=7,
                           solution_vector=solution_vector, optimization_side="min",
                           HMCR=0.6, PAR=0.3, population_size=30, epochs=50)
hs.run()

print(f'Best Global Objective Value: {hs.global_best_objective_value}')
print(f'Best Global Solution: {hs.global_best_solution}')
