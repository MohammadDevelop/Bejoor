from bejoor.swarm_based import FireworksAlgorithm
import math

def rosenbrock_function(sol):
    return sum(100 * (sol[i+1] - sol[i]**2)**2 + (sol[i] - 1)**2 for i in range(len(sol) - 1))

solution_vector = [{"type": "float", "lower_bound": -5, "upper_bound": 10}] * 7

fwa = FireworksAlgorithm(objective_function=rosenbrock_function, solution_vector_size=7,
                         solution_vector=solution_vector, optimization_side="min",
                         explosion_strength=60, sparks_per_firework=40, population_size=300, epochs=50)
fwa.run()

print(f'Best Global Objective Value: {fwa.global_best_objective_value}')
print(f'Best Global Solution: {fwa.global_best_solution}')