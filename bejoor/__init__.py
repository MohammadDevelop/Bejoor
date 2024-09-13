from .genetic import ToyGeneticAlgorithm, BaseGeneticAlgorithm
from .swarm_based import SalpSwarmAlgorithm, BatAlgorithm
from .physics_based import SimulatedAnnealing


genetic_based_algorithms = ['ToyGeneticAlgorithm', 'BaseGeneticAlgorithm']
swarm_based_algorithms = ['SalpSwarmAlgorithm', 'BatAlgorithm']
physics_based_algorithms = ['SimulatedAnnealing']

__all__ = (genetic_based_algorithms +
           swarm_based_algorithms +
           physics_based_algorithms)

