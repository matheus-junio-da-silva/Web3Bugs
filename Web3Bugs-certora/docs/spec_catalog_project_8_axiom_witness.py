"""Project 8: arithmetic sanity, not a Certora Prover run."""
import sympy as sp
z=sp.symbols("rayMul_g_1_0",real=True)
assert sp.satisfiable(sp.And(sp.Eq(z,0),sp.Ge(z,1)),use_lra_theory=True) is False
assert not (0*0 < 0*0+0)   # W2 rounding=0, denominator=0
assert not (0*0 < 0*0)     # W2 rounding=1, denominator=0
assert not (0 < 0)         # W3 rayDiv x=y=0
print("W1 UNSAT; W2 (0/1) false; W3 false; NOT CERTORA")
