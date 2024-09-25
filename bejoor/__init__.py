from .genetic import ToyGeneticAlgorithm, BaseGeneticAlgorithm, MemeticAlgorithm, BarnaclesMatingOptimizer
from .swarm_based import SalpSwarmAlgorithm, BatAlgorithm, ArtificialBeeColony, FireflyAlgorithm, FireworksAlgorithm, \
    WhaleOptimizationAlgorithm, FishSchoolingAlgorithm
from .physics_based import SimulatedAnnealing, GravitationalSearchAlgorithm, ElectromagneticFieldOptimization, \
    GalaxyBasedSearchAlgorithm
from .population_based import DifferentialEvolution, HarmonySearch, cuckoo_search, SineCosineAlgorithm
from .economics_based import ExchangeMarketAlgorithm
from .diophantine import DiophantineEquation

genetic_based_algorithms = ['ToyGeneticAlgorithm', 'BaseGeneticAlgorithm', 'MemeticAlgorithm',
                            'BarnaclesMatingOptimizer']
swarm_based_algorithms = ['SalpSwarmAlgorithm', 'BatAlgorithm', 'ArtificialBeeColony', 'FireflyAlgorithm',
                          'FireworksAlgorithm', 'WhaleOptimizationAlgorithm', 'FishSchoolingAlgorithm' ]
physics_based_algorithms = ['SimulatedAnnealing', 'GravitationalSearchAlgorithm', 'ElectromagneticFieldOptimization',
                            'GalaxyBasedSearchAlgorithm']
population_based_algorithms = ['DifferentialEvolution', 'HarmonySearch', 'cuckoo_search', 'SineCosineAlgorithm']
economics_based_algorithms = ['ExchangeMarketAlgorithm']
diophantine_algorithms = ['DiophantineEquation']

__all__ = (genetic_based_algorithms +
           swarm_based_algorithms +
           physics_based_algorithms +
           population_based_algorithms +
           economics_based_algorithms +
           diophantine_algorithms)
