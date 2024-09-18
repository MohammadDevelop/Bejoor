from bejoor.diophantine.Diophantine import DiophantineEquation
from bejoor.genetic import BaseGeneticAlgorithm

# Define a system of Diophantine equations
equation_system = [
    "x1**3 + 2*x2 = 100",
    "x1 + 3*x2**3 = 300"
]

# Define bounds for the variables
lower_bounds = [-50] * 3
upper_bounds = [50] * 3

# Create a DiophantineEquation instance
diophantine_eq = DiophantineEquation(equation_system, num_variables=3, lower_bound=lower_bounds, upper_bound=upper_bounds)

best_solution, best_objective_value = diophantine_eq.solve(BaseGeneticAlgorithm, population_size=300, epochs=200)

print("Best solution:", best_solution)
print("Best objective value:", best_objective_value)
