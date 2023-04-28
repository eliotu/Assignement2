from BeliefBase import BeliefBase
from sympy import *
from sympy import Symbol, sympify
from Belief import Belief
from sympy.abc import p,q,r,s


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    belief_base = BeliefBase()
    P = Symbol('P')
    R = Symbol('R')
    S = Symbol('S')
    Q = Symbol('Q')

    formula= Equivalent(r, Or(p, s))
    f=Implies(s,p)
    f2=Implies(s,q)

    belief_base.add_formula(Belief(f,1))
    belief_base.add_formula(Belief(f2,1))
    belief_base.add_formula(Belief(s,2))

    phi=~P




    formulas = belief_base.get_formulas()
    print(formulas)



    belief_base.contract(Belief(q,1))
    print(belief_base.get_formulas())
