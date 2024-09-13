from bejoor.swarm_based import FireflyAlgorithm
import math

def rosenbrock_function(sol):
    return sum(100 * (sol[i+1] - sol[i]**2)**2 + (sol[i] - 1)**2 for i in range(len(sol) - 1))

solution_vector = [{"type": "float", "lower_bound": -5, "upper_bound": 10}] * 7

fa = FireflyAlgorithm(objective_function=rosenbrock_function, solution_vector_size=7,
                         solution_vector=solution_vector, optimization_side="min",
                         alpha=0.2, beta_0=1.0, gamma=1.0, population_size=300, epochs=50)
fa.run()

print(f'Best Global Objective Value: {fa.global_best_objective_value}')
print(f'Best Global Solution: {fa.global_best_solution}')
