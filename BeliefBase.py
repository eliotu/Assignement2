from collections import deque

from sympy import *
from sympy import symbols, Not

from Belief import Belief

class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def add_formula(self, formula):
        if not self.contains(formula):
            self.beliefs.append(formula)

    def remove_formula(self, formula):
        if self.contains(formula):
            self.beliefs.remove(formula)

    def contains(self, formula):
        return formula in self.beliefs

    def get_beliefs(self):
        return self.beliefs
    def get_formulas(self):
        formulas=[f.formula for f in self.beliefs]

        return formulas


    ####################################################################


    #design and implementation of a method for checking logical entailment (e.g.resolution-
    #based), you should implement it yourself, without using any existing packages;

    def transform_to_cnf(self, formulas, phi):
        clauses = set()
        for formula in formulas:
            cnf_formula = to_cnf(formula.formula)
            if isinstance(cnf_formula, And):
                clauses |= set(cnf_formula.args)
            else:
                clauses.add(cnf_formula)
        if (phi is not None):
            cnf_phi = to_cnf(~(phi.formula))
            if isinstance(cnf_phi, And):
                clauses |= set(cnf_phi.args)
            else:
                clauses.add(cnf_phi)

        return clauses


    def resolution(self,phi):
        clauses=self.transform_to_cnf(self.beliefs, phi)
        while True:
            new_clauses = set()
            pairs = [(C1, C2) for C1 in clauses for C2 in clauses if C1 != C2]
            for (C1, C2) in pairs:
                r=self.find_new(C1,C2)
                if '' in r:  # if the list constains an empty clause
                    return True
                new_clauses=new_clauses.union(set(r))



            if new_clauses.issubset(clauses):
                return False

            clauses |= new_clauses

    def resolution_with_clauses(self,formulas, phi):
        clauses=self.transform_to_cnf(formulas,phi)
        while True:
            new_clauses = set()
            pairs = [(C1, C2) for C1 in clauses for C2 in clauses if C1 != C2]
            for (C1, C2) in pairs:
                r = self.find_new(C1, C2)
                if '' in r:  # if the list constains an empty clause
                    return True
                new_clauses = new_clauses.union(set(r))

            if new_clauses.issubset(clauses):
                return False

            clauses |= new_clauses

    def find_new(self, claus1,claus2):
        """ Resolves each pair and erases contradictions if possible """
        resolvents = []

        c1 = str(claus1).replace(" ", "").split("|")
        c2 = str(claus2).replace(" ", "").split("|")

        for i in c1:
            for j in c2:

                j_negate = str(Not(j))
                if i == j_negate:
                    temp_c1 = c1
                    temp_c2 = c2
                    [temp_c1.remove(i) for xi in temp_c1 if xi == i]
                    [temp_c2.remove(j) for xj in temp_c2 if xj == j]
                    temp_clause = temp_c1 + temp_c2

                    temp_clause = list(set(temp_clause))
                    temp_clause = "|".join(temp_clause)
                    resolvents.append(temp_clause)


        return resolvents


    ####################################################################


    def sort_by_priority(self, beliefs):
        s=sorted(beliefs, key=lambda x: x.priority, reverse=False)
        return s

    def contract(self, phi):
        """ Apply aging-based contraction with entrenchment to the belief base """

        prop_cnf = to_cnf(phi.formula)
        # Sort the beliefs in B in increasing order of priority.
        beliefs=self.sort_by_priority(self.beliefs)

        delete = []

        for i, belief in enumerate(beliefs):

            if self.resolution_with_clauses(beliefs[i:i + 1], Belief(prop_cnf,phi.priority)):
                delete.append(belief)

        self.beliefs = [belief for belief in self.beliefs if belief not in delete]

        # Iterate over each pair of beliefs in B
        for i, b1 in enumerate(self.beliefs):
            for j, b2 in enumerate(self.beliefs):
                if i == j:
                    continue
                # Check if beliefs b1 and b2 are inconsistent
                a=[b1]
                if not self.resolution_with_clauses([b1], b2) and not self.resolution_with_clauses([b2], b1):
                    # Remove the belief with lower priority
                    if b1.priority < b2.priority:
                        self.beliefs.pop(j)
                    else:
                        self.beliefs.pop(i)
                        break

