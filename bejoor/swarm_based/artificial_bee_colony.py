import random
from bejoor.core.bejoor_algorithm import BejoorAlgorithm
from bejoor.core.individual import Individual

class ArtificialBeeColony(BejoorAlgorithm):
    def __init__(self, *args, onlooker_bees=10, employed_bees=10, limit=100, **kwargs):
        """
        Artificial Bee Colony algorithm.
        :param onlooker_bees: Number of onlooker bees.
        :param employed_bees: Number of employed bees.
        :param limit: Limit for abandonment of a solution.
        """
        super().__init__(*args, **kwargs)
        self.onlooker_bees = onlooker_bees
        self.employed_bees = employed_bees
        self.limit = limit
        self.trial_counter = [0] * self.population_size
        self.optimizer_name = "Artificial Bee Colony"

    def employed_bee_phase(self):
        """Employed bees explore the neighborhood of their food source."""
        for i in range(self.employed_bees):
            candidate = self.generate_candidate(i)
            candidate_objective = self.objective_function(candidate)

            if (self.optimization_side == 'min' and candidate_objective < self.population[i].get_objective_value()) or \
               (self.optimization_side == 'max' and candidate_objective > self.population[i].get_objective_value()):
                self.population[i].set_values(candidate)
                self.population[i].set_objective_value(candidate_objective)
                self.trial_counter[i] = 0
            else:
                self.trial_counter[i] += 1

    def onlooker_bee_phase(self):
        """Onlooker bees probabilistically choose food sources based on quality."""
        fitness = [1 / (ind.get_objective_value() + 1e-10) for ind in self.population]
        total_fitness = sum(fitness)
        probabilities = [f / total_fitness for f in fitness]

        for _ in range(self.onlooker_bees):
            selected_index = random.choices(range(self.population_size), probabilities)[0]
            candidate = self.generate_candidate(selected_index)
            candidate_objective = self.objective_function(candidate)

            if (self.optimization_side == 'min' and candidate_objective < self.population[selected_index].get_objective_value()) or \
               (self.optimization_side == 'max' and candidate_objective > self.population[selected_index].get_objective_value()):
                self.population[selected_index].set_values(candidate)
                self.population[selected_index].set_objective_value(candidate_objective)

    def scout_bee_phase(self):
        """Replace abandoned solutions with new random solutions."""
        for i in range(self.population_size):
            if self.trial_counter[i] > self.limit:
                new_values = [random.uniform(self.solution_vector[j]['lower_bound'], self.solution_vector[j]['upper_bound'])
                              for j in range(self.solution_vector_size)]
                self.population[i].set_values(new_values)
                self.population[i].set_objective_value(self.objective_function(new_values))
                self.trial_counter[i] = 0

    def generate_candidate(self, index):
        """Generate a candidate solution by modifying the current one."""
        candidate = self.population[index].get_values()[:]
        partner_index = random.choice([i for i in range(self.population_size) if i != index])
        phi = random.uniform(-1, 1)
        for i in range(self.solution_vector_size):
            candidate[i] = candidate[i] + phi * (candidate[i] - self.population[partner_index].values[i])
            candidate[i] = min(max(candidate[i], self.solution_vector[i]['lower_bound']), self.solution_vector[i]['upper_bound'])
        return candidate

    def update(self):
        """Execute the employed, onlooker, and scout bee phases."""
        self.employed_bee_phase()
        self.onlooker_bee_phase()
        self.scout_bee_phase()
        self.evaluate_all_objectives()
        self.sort_individuals()
