from bejoor.swarm_based import ArtificialBeeColony
import math

def ackley_function(sol):
    n = len(sol)
    term1 = -20 * math.exp(-0.2 * math.sqrt(sum(x**2 for x in sol) / n))
    term2 = -math.exp(sum(math.cos(2 * math.pi * x) for x in sol) / n)
    return term1 + term2 + 20 + math.e

solution_vector = [{"type": "float", "lower_bound": -32.768, "upper_bound": 32.768}] * 7

abc = ArtificialBeeColony(objective_function=ackley_function, solution_vector_size=7,
                          solution_vector=solution_vector, optimization_side="min",
                          onlooker_bees=10, employed_bees=10, limit=100, population_size=300, epochs=50)
abc.run()

print(f'Best Global Objective Value: {abc.global_best_objective_value}')
print(f'Best Global Solution: {abc.global_best_solution}')
