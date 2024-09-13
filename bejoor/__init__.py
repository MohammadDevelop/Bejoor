from .genetic import ToyGeneticAlgorithm, BaseGeneticAlgorithm, MemeticAlgorithm
from .swarm_based import SalpSwarmAlgorithm, BatAlgorithm, ArtificialBeeColony, FireflyAlgorithm
from .physics_based import SimulatedAnnealing, GravitationalSearchAlgorithm
from .population_based import DifferentialEvolution, HarmonySearch, cuckoo_search

genetic_based_algorithms = ['ToyGeneticAlgorithm', 'BaseGeneticAlgorithm', 'MemeticAlgorithm']
swarm_based_algorithms = ['SalpSwarmAlgorithm', 'BatAlgorithm', 'ArtificialBeeColony', 'FireflyAlgorithm']
physics_based_algorithms = ['SimulatedAnnealing', 'GravitationalSearchAlgorithm']
population_based_algorithms = ['DifferentialEvolution', 'HarmonySearch', 'cuckoo_search']

__all__ = (genetic_based_algorithms +
           swarm_based_algorithms +
           physics_based_algorithms +
           population_based_algorithms)

