from bejoor.economics_based import SupplyDemandOptimization

def rosenbrock_function(sol):
    return sum(100 * (sol[i+1] - sol[i]**2)**2 + (sol[i] - 1)**2 for i in range(len(sol) - 1))

solution_vector = [{"type": "float", "lower_bound": -5, "upper_bound": 10}] * 7

optimizer = SupplyDemandOptimization(objective_function=rosenbrock_function, solution_vector_size=7,
                                     solution_vector=solution_vector, optimization_side="min",
                                     supply_probability=0.75, population_size=50, epochs=50)
optimizer.run()

print(f'Best Global Objective Value: {optimizer.global_best_objective_value}')
print(f'Best Global Solution: {optimizer.global_best_solution}')
