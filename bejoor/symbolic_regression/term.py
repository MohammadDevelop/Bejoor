import math


class Term:
    def __init__(self, term_type, constant_list=None, operand_list=None):
        """
        Initialize a term in the symbolic regression model.

        Parameters:
        - term_type: str, the type of the function (e.g., 'sin', 'cos', 'log').
        - constant_list: list of float, constants that the term may use.
        - operand_list: list of string.
        """
        self.term_type = term_type
        self.constant_list = constant_list if constant_list is not None else []
        self.operand_list = operand_list if operand_list is not None else []

    def term_string(self):
        if self.term_type =="const":
            term_string_= "C0"
        elif self.term_type in ["sin","cos","tan"]:
            term_string_= f"{self.term_type}({self.operand_list[0]})"
        elif self.term_type in ["log"]:
            term_string_= f"{self.term_type}({self.operand_list[0]},{self.operand_list[1]})"

        for i in range(0,len(self.constant_list)):
            term_string_=term_string_.replace(f"C{i}",str(self.constant_list[i]))

        return term_string_
        # If type is unknown, raise an error
        raise ValueError(f"Unknown term type: {self.term_type}")