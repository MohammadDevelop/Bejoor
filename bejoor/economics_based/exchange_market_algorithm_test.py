from bejoor.economics_based import ExchangeMarketAlgorithm

def rosenbrock_function(sol):
    return sum(100 * (sol[i+1] - sol[i]**2)**2 + (sol[i] - 1)**2 for i in range(len(sol) - 1))

solution_vector = [{"type": "float", "lower_bound": -5, "upper_bound": 10}] * 7

ema = ExchangeMarketAlgorithm(objective_function=rosenbrock_function, solution_vector_size=7,
                              solution_vector=solution_vector, optimization_side="min",
                              trading_probability=0.8, population_size=50, epochs=50)
ema.run()

print(f'Best Global Objective Value: {ema.global_best_objective_value}')
print(f'Best Global Solution: {ema.global_best_solution}')
