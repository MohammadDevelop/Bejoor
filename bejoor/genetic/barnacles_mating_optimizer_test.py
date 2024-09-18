from bejoor.genetic import BarnaclesMatingOptimizer
import math
def rastrigin_function(sol):
    n = len(sol)
    return 10 * n + sum(x**2 - 10 * math.cos(2 * math.pi * x) for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

bmo = BarnaclesMatingOptimizer(objective_function=rastrigin_function, solution_vector_size=7,
                               solution_vector=solution_vector, optimization_side="min",
                               mating_rate=0.7, growth_rate=0.15, population_size=100, epochs=50)
bmo.run()

print(f'Best Global Objective Value: {bmo.global_best_objective_value}')
print(f'Best Global Solution: {bmo.global_best_solution}')
