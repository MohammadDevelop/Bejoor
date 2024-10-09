from bejoor.economics_based import ExchangeMarketAlgorithm

def sphere_function(sol):
    return sum(x**2 for x in sol)


solution_vector = [{"type": "float", "lower_bound": -5, "upper_bound": 10}] * 7

ema = ExchangeMarketAlgorithm(objective_function=sphere_function, solution_vector_size=7,
                              solution_vector=solution_vector, optimization_side="min",
                              trading_probability=0.8, population_size=250, epochs=50)
ema.run()

print(f'Best Global Objective Value: {ema.global_best_objective_value}')
print(f'Best Global Solution: {ema.global_best_solution}')
