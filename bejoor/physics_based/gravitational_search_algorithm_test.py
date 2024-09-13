from bejoor.physics_based import GravitationalSearchAlgorithm

def sphere_function(sol):
    return sum(x**2 for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

gsa = GravitationalSearchAlgorithm(objective_function=sphere_function, solution_vector_size=7,
                           solution_vector=solution_vector, optimization_side="min",
                           G_initial=100, G_decay=0.99, population_size=30, epochs=50)
gsa.run()

print(f'Best Global Objective Value: {gsa.global_best_objective_value}')
print(f'Best Global Solution: {gsa.global_best_solution}')

