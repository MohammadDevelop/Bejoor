from bejoor.swarm_based import SalpSwarmAlgorithm

def func(sol):
    return abs( (sol[0]**sol[3] + sol[1]**sol[3] - sol[2]**sol[3]))


solution_vector =  [{"type": "integer", "lower_bound": 1, "upper_bound": 500}] * 3 + \
                   [{"type": "integer", "lower_bound": 2, "upper_bound": 100}] + \
                   [{"type": "float", "lower_bound": 0, "upper_bound": 1}] * 3


# without target objective value
ssa= SalpSwarmAlgorithm(objective_function=func, solution_vector_size=7,
                        solution_vector=solution_vector, optimization_side="min",
                        c_1=2, population_size=500, epochs=200)
ssa.run()

print(ssa.best_solution)
print(ssa.best_objective_value)

# specified target objective value
ssa= SalpSwarmAlgorithm(objective_function=func, solution_vector_size=7,
                        solution_vector=solution_vector, optimization_side="min",
                        target_objective_value=0, c_1=2, population_size=500, epochs=200)
ssa.run()

print(ssa.best_solution)
print(ssa.best_objective_value)