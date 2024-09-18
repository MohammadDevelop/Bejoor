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
### Basic Parameters of Optimizers:
- objective_function: Objective function needs to be optimized.
- solution_vector_size: Vector size of the candidate solutions.
- solution_vector: A vector which determines the types of each variable in solution vectors.
- optimization_side: Determines maximize or minimize the objective function.
- target_objective_value: Target Objective value.
- target_objective_lower_bound: Target Objective lower bound.
- target_objective_upper_bound: Target Objective upper bound.
- population_size: Number of individuals in the population
- epochs: Number of generations to run the algorithm


[//]: # (## Support the Project)

[//]: # (If you find this project useful and would like to support its continued development, feel free to make a donation:)

[//]: # ()
[//]: # (- **Bitcoin &#40;BTC&#41;**: `your-bitcoin-address-here`)

[//]: # (- **Ethereum &#40;ETH&#41;**: `your-ethereum-address-here`)

[//]: # (- **Litecoin &#40;LTC&#41;**: `your-litecoin-address-here`)

[//]: # (- **Tron &#40;TRX&#41;**: `your-litecoin-address-here`)

[//]: # ()
[//]: # (Any contribution is greatly appreciated!)
