from bejoor.symbolic_regression import Term
from bejoor.symbolic_regression import SymbolicRegressor
import math

t= Term(term_type="sin",constant_list=[90],operand_list=["C0"])

print(t.term_string())

t1= Term(term_type="log",constant_list=[10],operand_list=["X0","C0"])

print(t1.term_string())


sr=SymbolicRegressor(term_list=[t,t1],operator_list=['+'])

print(sr.total_string())

print(sr.predict_single([100]))

print(math.sin(90))