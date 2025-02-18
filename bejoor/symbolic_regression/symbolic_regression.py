import math
from bejoor.genetic import *
from bejoor.symbolic_regression import Term


class SymbolicRegressor:
    def __init__(self, term_list=None, operator_list=None, max_terms=10, max_const=5):
        """
        Initialize a symbolic regressor model.

        Parameters:
        - term_list: list of Terms.
        - operator_list: list of strings ('+', '-', '*', '/', '**').
        """
        # Ensure term_list and operator_list meet the required length condition
        if term_list is not None and operator_list is not None:
            if len(operator_list) != len(term_list) - 1:
                raise ValueError("The length of operator_list must be one less than the length of term_list.")

        self.max_terms = max_terms
        self.max_const = max_const
        self.term_list = term_list if term_list is not None else []
        self.operator_list = operator_list if operator_list is not None else []
        self.model_string = self.total_string()

    def total_string(self):
        total_string_ = ""
        for i, term in enumerate(self.term_list):
            total_string_ += f"({term.term_string()})"
            if i < len(self.operator_list):
                total_string_ += f" {self.operator_list[i]} "
        return total_string_

    def total_string_candidate(self, candidate_sol):
        """
        Generate a model string based on a candidate solution.
        """
        terms = []
        n = self.max_terms

        for i in range(self.max_terms):
            term_type = candidate_sol[i]
            operand_1 = candidate_sol[2 * n + 2 * i]
            operand_2 = candidate_sol[2 * n + 2 * i + 1]
            constants = candidate_sol[self.max_terms:self.max_terms + self.max_const]
            terms.append(Term(term_type=term_type, operand_list=[operand_1, operand_2], constant_list=constants))

        operators = candidate_sol[self.max_terms:self.max_terms + self.max_terms - 1]
        total_string_ = ""

        for i, term in enumerate(terms):
            total_string_ += f"({term.term_string()})"
            if i < len(operators):
                total_string_ += f" {operators[i]} "
        return total_string_

    def predict_single(self, input_vector, candidate_model_string=None):
        eval_str = candidate_model_string if candidate_model_string is not None else self.model_string

        for i in range(len(input_vector)):
            eval_str = eval_str.replace(f"X{i}", str(input_vector[i]))

        safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'exp': math.exp,
            '**': pow,
        }

        try:
            return eval(eval_str, {"__builtins__": None}, safe_dict)
        except Exception as e:
            print(f"Error evaluating expression: {e}")
            return float('inf')  # High value for error cases

    def predict(self, X, candidate_model_string=None):
        return [self.predict_single(sample, candidate_model_string) for sample in X]

    def mse_loss(self, solution, X, y):
        """
        Calculate the mean squared error loss for a candidate solution.

        Parameters:
        - solution: The candidate solution vector.
        - X: Input data.
        - y: Ground truth labels.

        Returns:
        - float: Mean squared error.
        """
        candidate_model_string = self.total_string_candidate(solution)
        predictions = self.predict(X, candidate_model_string)
        return sum((p - t) ** 2 for p, t in zip(predictions, y)) / len(y)

    def fit(self, X, y):
        """
        Fit the symbolic regression model to the data using a genetic algorithm.

        Parameters:
        - X: Input features (2D list or numpy array).
        - y: Target values (1D list or numpy array).
        """
        feature_num = len(X[0])
        feature_strings = [f"X{i}" for i in range(feature_num)]
        const_strings = [f"C{i}" for i in range(self.max_const)]

        solution_vector = (
            [{"type": "string", "possible_values": ["sin", "cos", "tan", "const", "log"]}] * self.max_terms +
            [{"type": "string", "possible_values": ["+", "-", "*", "/", "**"]}] * (self.max_terms - 1) +
            [{"type": "string", "possible_values": feature_strings + const_strings}] * (self.max_terms * 2)
        )

        def func(solution):
            return self.mse_loss(solution, X, y)

        bga = BaseGeneticAlgorithm(
            objective_function=func,
            solution_vector_size=len(solution_vector),
            solution_vector=solution_vector,
            optimization_side="min",
            target_objective_upper_bound=1e-5,
            crossover_probability=0.9,
            mutation_probability=0.1,
            elitism_rate=0.05,
            selection_strategy="tournament",
            crossover_type="one-point",
            population_size=500,
            epochs=200
        )
        bga.run()

        # Store the best solution
        best_solution = bga.best_solution
        self.model_string = self.total_string_candidate(best_solution)
        print(f"Best Model: {self.model_string}")
