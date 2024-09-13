from bejoor.swarm_based import BatAlgorithm

def func(sol):
    return abs((sol[0]**sol[3] + sol[1]**sol[3] - sol[2]**sol[3]))


solution_vector =  [{"type": "integer", "lower_bound": 1, "upper_bound": 500}] * 3 + \
                   [{"type": "integer", "lower_bound": 2, "upper_bound": 100}] + \
                   [{"type": "float", "lower_bound": 0, "upper_bound": 1}] * 3


# without target objective value
ba= BatAlgorithm(objective_function=func, solution_vector_size=7,
                 solution_vector=solution_vector, optimization_side="min",
                 loudness=0.3, pulse_rate=0.5, min_frequency=0.0, max_frequency=2.0,
                 population_size=30, epochs=50)
ba.run()

print(ba.best_solution)
print(ba.best_objective_value)
