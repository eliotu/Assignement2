from sympy import symbols
from BeliefBase import BeliefBase
from Belief import Belief
from sympy import symbols, Not,And

from sympy.abc import p,q,r,s

# Create some symbolic variables for testing




def check_success(belief_base,phi):
    # checking if phi belongs to the belief base  after revision
    belief_base.revision(phi)
    return belief_base.contains(phi)

def check_inclusion(belief_base,phi):
    other_belief_base=belief_base.copy()
    belief_base.revision(phi)
    other_belief_base.add_formula(phi)
    tmp=True
    formulas=belief_base.get_beliefs()
    for f in formulas:
        if not other_belief_base.contains(f):
            tmp=False
    return tmp

def check_vacuity(belief_base,phi):
    n_phi= Belief(Not(phi.formula),phi.priority)
    if not belief_base.contains(n_phi):
        new_belief=belief_base.copy()
        belief_base.revision(phi)
        new_belief.expand(phi)
        print(belief_base.get_formulas())
        print(new_belief.get_formulas())

        return belief_base==new_belief


def check_consistency(belief_base,phi):
    pass

def check_extensionality(belief_base,phi):
    pass




##check success
B = {Belief(p, 3), Belief(p | q, 2), Belief(~q, 1)}
f = Belief(p & q, 2)
belief_base = BeliefBase()
for belief in B:
    belief_base.add_formula(belief)
result = check_success(belief_base, f)
print(result)

##check inclusion
belief_base = BeliefBase()
belief_base.add_formula(Belief(p, 1))
belief_base.add_formula(Belief(~q | r, 2))
belief_base.add_formula(Belief(r | s, 3))

phi = Belief(And(p, q), 4)
is_included = check_inclusion(belief_base, phi)
print(is_included)


##check vacuity
belief_base = BeliefBase()
belief_base.add_formula(Belief(p, 1))
belief_base.add_formula(Belief(~q | r, 2))

phi=Belief(s,3)
is_vacuity=check_vacuity(belief_base,phi)
print(is_vacuity)