from toy_genetic import ToyGeneticAlgorithm

def func(sol):
    return abs( (sol[len(sol)-1]**2 + sol[len(sol)-3]**2 - sol[len(sol)-4]**2) - 300)


solution_vector= ([{"type":"string", "possible_values":["a","b","c"]}]
    +[{"type": "float", "lower_bound": 0, "upper_bound": 1}] *2
    +[{"type": "integer", "lower_bound": 0, "upper_bound": 100 }] *2)


tga= ToyGeneticAlgorithm(objective_function=func, solution_vector_size=5,
                         solution_vector=solution_vector,
                         optimization_side="min", population_size=200, epochs=100)

tga.run()


print(tga.best_solution)
print(tga.best_objective_value)