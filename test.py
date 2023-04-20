from sympy.abc import p, q, r,s
from sympy import *
import pytest
from BeliefBase import BeliefBase


@pytest.fixture
def belief_base():
    bb = BeliefBase()
    bb.add_formula(p)
    bb.add_formula(Implies(p, q))
    bb.add_formula(Implies(q, r))
    return bb


def test_resolution_entailment(belief_base):
    phi = r
    assert belief_base.resolution(phi) == True


def test_resolution_non_entailment(belief_base):
    phi = Not(s)
    assert belief_base.resolution(phi) == True

