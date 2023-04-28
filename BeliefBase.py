from collections import deque

from sympy import *
from sympy import symbols, Not

from Belief import Belief

class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def __eq__(self, other):
        if(len(other.get_beliefs())==len(self.beliefs)):
            for c in other.get_beliefs():
                if not self.contains(c):
                    return false
            return true

        return false


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

    def copy(self):
        new=BeliefBase()
        for b in self.get_beliefs():
            new.add_formula(b)
        return new

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


    def entailement(self,phi):
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

    def entailement_with_clauses(self,formulas, phi):
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


    def sort_by_priority(self, beliefs,reverse=True):
        s=sorted(beliefs, key=lambda x: x.priority, reverse=reverse)
        return s



    def contract(self, phi):
        """ Apply aging-based contraction with entrenchment to the belief base """

        prop_cnf = to_cnf(phi.formula)
        # Sort the beliefs in B in increasing order of priority.
        beliefs=self.sort_by_priority(self.beliefs)

        tmp_beliefs = []

        for i, belief in enumerate(beliefs):
            tmp_beliefs.append(belief)
            # Check if the conjunction of the beliefs in tmp_beliefs and the new belief (phi)
            # entails the new belief. If so, remove the new belief from tmp_beliefs.
            if self.entailement_with_clauses(tmp_beliefs,Belief(prop_cnf,phi.priority)):
                tmp_beliefs.pop()



        self.beliefs = tmp_beliefs

        # Iterate over each pair of beliefs in B



    ####################################################################
    def expand(self, phi):

        self.add_formula(phi)


    def revision(self,phi):
        ## we are going to use levi-identity
        negated_cnf = Belief(Not(to_cnf(phi.formula)),phi.priority)
        self.contract(negated_cnf)
        self.expand(phi)


