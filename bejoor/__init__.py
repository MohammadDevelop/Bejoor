from .genetic import ToyGeneticAlgorithm, BaseGeneticAlgorithm, MemeticAlgorithm
from .swarm_based import SalpSwarmAlgorithm, BatAlgorithm, ArtificialBeeColony, FireflyAlgorithm, FireworksAlgorithm,\
    WhaleOptimizationAlgorithm
from .physics_based import SimulatedAnnealing, GravitationalSearchAlgorithm, ElectromagneticFieldOptimization, \
    GalaxyBasedSearchAlgorithm
from .population_based import DifferentialEvolution, HarmonySearch, cuckoo_search, SineCosineAlgorithm

genetic_based_algorithms = ['ToyGeneticAlgorithm', 'BaseGeneticAlgorithm', 'MemeticAlgorithm']
swarm_based_algorithms = ['SalpSwarmAlgorithm', 'BatAlgorithm', 'ArtificialBeeColony', 'FireflyAlgorithm',
                          'FireworksAlgorithm', 'WhaleOptimizationAlgorithm']
physics_based_algorithms = ['SimulatedAnnealing', 'GravitationalSearchAlgorithm', 'ElectromagneticFieldOptimization',
                            'GalaxyBasedSearchAlgorithm']
population_based_algorithms = ['DifferentialEvolution', 'HarmonySearch', 'cuckoo_search', 'SineCosineAlgorithm']

__all__ = (genetic_based_algorithms +
           swarm_based_algorithms +
           physics_based_algorithms +
           population_based_algorithms)

