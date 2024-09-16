from bejoor.physics_based import ElectromagneticFieldOptimization

def sphere_function(sol):
    return sum(x**2 for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

efo = ElectromagneticFieldOptimization(objective_function=sphere_function, solution_vector_size=7,
                           solution_vector=solution_vector, optimization_side="min",
                           charge_intensity=1, population_size=30, epochs=50)
efo.run()

print(f'Best Global Objective Value: {efo.global_best_objective_value}')
print(f'Best Global Solution: {efo.global_best_solution}')
