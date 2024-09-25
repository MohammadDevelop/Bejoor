from bejoor.swarm_based import FishSchoolingAlgorithm
import math

def rosenbrock_function(sol):
    return sum(100 * (sol[i+1] - sol[i]**2)**2 + (sol[i] - 1)**2 for i in range(len(sol) - 1))

solution_vector = [{"type": "float", "lower_bound": -5, "upper_bound": 10}] * 7

optimizer = FishSchoolingAlgorithm(objective_function=rosenbrock_function, solution_vector_size=7,
                                   solution_vector=solution_vector, optimization_side="min",
                                   visual_range=0.2, step_individual=0.01, step_volitive=0.02,
                                   population_size=300, epochs=50)
optimizer.run()

print(f'Best Global Objective Value: {optimizer.global_best_objective_value}')
print(f'Best Global Solution: {optimizer.global_best_solution}')