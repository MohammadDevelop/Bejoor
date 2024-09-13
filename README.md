# Bejoor

This package is a collection of optimization algorithms. The aim is high diversity of optimizers and eased of use. 

For documentation, [Visit this](https://amzmohammad.com/bejoor/).

## Installation
    pip install bejoor

# Sample Usage
```python
from bejoor.genetic import BaseGeneticAlgorithm

def func(sol):
    return abs((sol[0]**sol[3] + sol[1]**sol[3] - sol[2]**sol[3]))


solution_vector =  [{"type": "integer", "lower_bound": 1, "upper_bound": 500}] * 3 + \
                   [{"type": "integer", "lower_bound": 2, "upper_bound": 100}] + \
                   [{"type": "float", "lower_bound": 0, "upper_bound": 1}] * 2 + \
                   [{"type": "string", "possible_values": ["option1", "option2", "option3"]}]

bga = BaseGeneticAlgorithm(objective_function=func, solution_vector_size=7,
                           solution_vector=solution_vector, optimization_side="min", target_objective_upper_bound=5,
                           crossover_probability=0.9, mutation_probability=0.1,
                           elitism_rate=0.05, selection_strategy="roulette",
                           crossover_type="one-point", population_size=500, epochs=200)

bga.run()

print(bga.best_solution)
print(bga.best_objective_value)
```
