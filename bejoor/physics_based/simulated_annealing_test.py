from bejoor.physics_based import SimulatedAnnealing

def func(sol):
    return (sol[1]**sol[0] + sol[2]**sol[0] - sol[3]**sol[0] - sol[4]**sol[0]) ** 2


solution_vector =  [{"type": "integer", "lower_bound": 2, "upper_bound": 10}] + \
                   [{"type": "float", "lower_bound": 0.0, "upper_bound": 1.0}] *4


# without target objective value
sa= SimulatedAnnealing(objective_function=func, solution_vector_size=5,
                 solution_vector=solution_vector, optimization_side="min",
                 initial_temperature=1000, cooling_rate=0.9,
                 population_size=10000, epochs=100)
sa.run()

print(f'Best Global Objective Value: {sa.global_best_objective_value}')
print(f'Best Global Solution: {sa.global_best_solution}')
