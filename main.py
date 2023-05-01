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


    option=-1
    while(option!=5):
        print("Print (1)")
        print("Contract (2)")
        print(" Expand (3)")
        print(" Revise (4)")
        print(" Exit (5)")
        option=int(input("What do you want to do:"))

        if(option==1):
            print(belief_base.get_formulas())
        elif(option==2):
            formula = input("Enter the formula:")
            priority = int(input("enter priority:"))
            f = Belief(sympify(formula), priority)
            belief_base.contract(f)
        elif (option == 3):
            formula = input("Enter the formula:")
            priority = int(input("enter priority:"))
            f = Belief(sympify(formula), priority)
            belief_base.expand(f)
        elif (option == 4):
            formula = input("Enter the formula:")
            priority = int(input("enter priority:"))
            f = Belief(sympify(formula), priority)
            belief_base.revision(f)
        else:
            print("Thank you")
            option=5





