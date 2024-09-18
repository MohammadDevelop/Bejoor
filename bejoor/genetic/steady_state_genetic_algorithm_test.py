from bejoor.genetic import  ToyGeneticAlgorithm, BaseGeneticAlgorithm, SteadyStateGeneticAlgorithm

def sphere_function(sol):
    return sum(x**2 for x in sol)

solution_vector = [{"type": "float", "lower_bound": -5.12, "upper_bound": 5.12}] * 7

ssga = SteadyStateGeneticAlgorithm(objective_function=sphere_function, solution_vector_size=7,
                                   solution_vector=solution_vector, optimization_side="min", target_objective_upper_bound=5,
                                   crossover_probability=0.9, mutation_probability=0.1,
                                   elitism_rate=0.05, selection_strategy="tournament", offspring_size=10,
                                   crossover_type="one-point", population_size=50, epochs=200)
ssga.run()

print(ssga.best_solution)
print(ssga.best_objective_value)