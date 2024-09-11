class Individual:
    def __init__(self, id, values):
        """
        Initialize an individual with an index and values (solution vector).

        :param index: Index of the individual in the population.
        :param values: The solution vector of the individual.
        """
        self.id = id
        self.values = values
        self.objective_value = None  # Will be set later after evaluation

    def get_index(self):
        """Get the index of the individual."""
        return self.id

    def set_index(self, index):
        """Set the index of the individual."""
        self.id = index

    def get_values(self):
        """Get the solution vector of the individual."""
        return self.values

    def set_values(self, values):
        """Set the solution vector of the individual."""
        self.values = values

    def get_objective_value(self):
        """Get the objective value of the individual."""
        return self.objective_value

    def set_objective_value(self, objective_value):
        """Set the objective value of the individual."""
        self.objective_value = objective_value
