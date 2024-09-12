

# Usage
```python
from bejoor.swarm_based import SalpSwarmAlgorithm

def func(sol):
    return abs( (sol[0]**sol[3] + sol[1]**sol[3] - sol[2]**sol[3]))


solution_vector =  [{"type": "integer", "lower_bound": 1, "upper_bound": 500}] * 3 + \
                   [{"type": "integer", "lower_bound": 2, "upper_bound": 100}] + \
                   [{"type": "float", "lower_bound": 0, "upper_bound": 1}] * 3


ssa= SalpSwarmAlgorithm(objective_function=func, solution_vector_size=7,
                        solution_vector=solution_vector, optimization_side="min",
                        c_1=2, population_size=500, epochs=200)

ssa.run()


print(ssa.best_solution)
print(ssa.best_objective_value)
```

# BibTeX citation to the algorithm:

```bibtex
@article{mirjalili2017salp,
  title={Salp Swarm Algorithm: A bio-inspired optimizer for engineering design problems},
  author={Mirjalili, Seyedali and Gandomi, Amir H and Mirjalili, Seyedeh Zahra and Saremi, Shahrzad and Faris, Hossam and Mirjalili, Seyed Mohammad},
  journal={Advances in engineering software},
  volume={114},
  pages={163--191},
  year={2017},
  publisher={Elsevier}
}
```

# More Available Resources about the algorithm:

[Salp swarm algorithm: a comprehensive survey](https://link.springer.com/article/10.1007/s00521-019-04629-4)