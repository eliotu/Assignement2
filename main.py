from BeliefBase import BeliefBase
from sympy import *
from sympy import Symbol, sympify
from Belief import Belief


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    belief_base = BeliefBase()
    P = Symbol('P')
    R = Symbol('R')
    S = Symbol('s')
    Q = Symbol('Q')

    formula= Equivalent(R,P | S)
    belief_base.add_formula(Belief(P,3))
    belief_base.add_formula(Belief(R,5))
    belief_base.add_formula(Belief(P&R,1))






    formulas = belief_base.get_formulas()
    print(formulas)



    belief_base.contract(Belief(P,4))
    print(belief_base.get_formulas())
