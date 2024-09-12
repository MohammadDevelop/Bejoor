from bejoor.genetic import  ToyGeneticAlgorithm

def func(sol):
    return abs( (sol[0]**sol[3] + sol[1]**sol[3] - sol[2]**sol[3]))


solution_vector =  [{"type": "integer", "lower_bound": 1, "upper_bound": 500}] * 3 + \
                   [{"type": "integer", "lower_bound": 2, "upper_bound": 100}] + \
                   [{"type": "float", "lower_bound": 0, "upper_bound": 1}] * 2 + \
                   [{"type": "string", "possible_values": ["option1", "option2", "option3"]}]

# without target objective value
tga= ToyGeneticAlgorithm(objective_function=func, solution_vector_size=7,
                         solution_vector=solution_vector, optimization_side="min",
                         mutation_probability=0.4, population_size=500, epochs=200)

tga.run()

print(tga.best_solution)
print(tga.best_objective_value)

# specified upper bound for objective value
solution_vector =  [{"type": "integer", "lower_bound": 1, "upper_bound": 500}] * 3 + \
                   [{"type": "integer", "lower_bound": 2, "upper_bound": 100}] + \
                   [{"type": "float", "lower_bound": 0, "upper_bound": 1}] * 2 + \
                   [{"type": "string", "possible_values": ["option1", "option2", "option3"]}]


tga= ToyGeneticAlgorithm(objective_function=func, solution_vector_size=7,
                         solution_vector=solution_vector, optimization_side="min", target_objective_upper_bound=1,
                         mutation_probability=0.4, population_size=500, epochs=200)

tga.run()

print(tga.best_solution)
print(tga.best_objective_value)