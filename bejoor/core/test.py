from bejoor_algorithm import BejoorAlgorithm

def func(sol):
    return abs( (sol[len(sol)-1]**2 + sol[len(sol)-3]**2 - sol[len(sol)-4]**2) - 300)


solution_vector= ([{"type":"string", "possible_values":["a","b","c"]}]
    +[{"type": "float", "lower_bound": 0, "upper_bound": 1}] *2
    +[{"type": "integer", "lower_bound": 0, "upper_bound": 100 }] *2)


bj= BejoorAlgorithm(objective_function=func, solution_vector_size=5, solution_vector=solution_vector ,
                    optimization_side="min", population_size=20, epochs=100)

bj.run()

# for ind in bj.population:
#     print(ind.values)
#     print(ind.objective_value)


print(bj.best_solution)
print(bj.best_objective_value)