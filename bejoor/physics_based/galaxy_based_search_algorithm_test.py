from bejoor.physics_based import GalaxyBasedSearchAlgorithm

def sphere_function(sol):
    return sum(x**2 for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

gbsa = GalaxyBasedSearchAlgorithm(objective_function=sphere_function, solution_vector_size=7,
                           solution_vector=solution_vector, optimization_side="min",
                           gravity_constant=0.02, population_size=300, epochs=50)
gbsa.run()

print(f'Best Global Objective Value: {gbsa.global_best_objective_value}')
print(f'Best Global Solution: {gbsa.global_best_solution}')
