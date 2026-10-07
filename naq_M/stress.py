"""Compare solution.solve against the brute force on random tiny graphs.
Run from the repo root:  python3 naq_M/stress.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from brute import count_brute
from gen import random_case
from solution import solve

for seed in range(500):
    n = 3 + seed % 8
    case = random_case(n, seed=seed)
    want = count_brute(*case)
    got = solve(*case)
    if want != got:
        print("MISMATCH", "seed", seed)
        print("n, k, vals, edges =", case)
        print("brute:", want, "yours:", got)
        sys.exit(1)
print("all 500 cases match")
