"""NAQ M (Tourism Balance): skeleton. Fill in the three TODO functions.

Plan (from the judges' slide):
  1. Find the cycle.
  2. Give every vertex a label: which cycle vertex's hanging tree it is in.
  3. Count pairs whose values differ by exactly k.
  answer = 2 * (qualifying pairs in whole graph) - (qualifying pairs inside the same tree)

ASSUMED INPUT (edit read_input to match the real statement):
  n k
  v_1 ... v_n
  n lines: a b   (1-indexed edges)
solve() uses 0-indexed vertices.
"""
import sys
from collections import deque, Counter


def find_cycle_vertices(n, adj):
    """TODO: return a list/set of the vertices that lie on the cycle.
    Hint: repeatedly remove degree-1 vertices (queue). Whatever is left is the cycle."""
    raise NotImplementedError


def label_trees(n, adj, cycle):
    """TODO: return label[v] = the cycle vertex whose hanging tree contains v.
    Hint: multi-source BFS starting from every cycle vertex at once; never step
    onto another cycle vertex."""
    raise NotImplementedError


def count_pairs(values, k):
    """TODO: number of unordered pairs (i < j) in `values` with abs difference == k.
    Hint: Counter. k == 0 needs c*(c-1)//2 per value; k > 0 needs cnt[v]*cnt[v+k]."""
    raise NotImplementedError


def solve(n, k, vals, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    cycle = find_cycle_vertices(n, adj)
    label = label_trees(n, adj, cycle)

    whole = count_pairs(vals, k)
    groups = {}
    for v in range(n):
        groups.setdefault(label[v], []).append(vals[v])
    same_tree = sum(count_pairs(g, k) for g in groups.values())

    return 2 * whole - same_tree


def read_input():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    vals = [int(x) for x in data[2:2 + n]]
    edges = []
    pos = 2 + n
    for _ in range(n):
        edges.append((int(data[pos]) - 1, int(data[pos + 1]) - 1))
        pos += 2
    return n, k, vals, edges


if __name__ == "__main__":
    print(solve(*read_input()))
