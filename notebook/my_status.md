# My status: what I know, and my own bugs

Built from my 2026 PacNW Div 1 contest and the solutions in the repo root. Update after every contest.

## My bug checklist (read before every submit)

Every line here is a bug I actually made.

| Check | Where it bit me |
|---|---|
| Loop bound for blocks of length 2^i: `j + 2^i <= n`, not `<` | `sparse.py`: last block per level never filled; my test `(0, 11)` hid it |
| No made-up filler values (`-67`). Use `inf` for min, or don't create the slot | `sparse.py`: wrong answer looked like a normal number |
| `[x for ...]` keeps its square brackets. Without them it's a generator: "not subscriptable" | PacNW K: crash in `sparse_query` |
| `int(math.log(x, 2))` is a float. Use `x.bit_length() - 1` | `sparse.py` |
| "modulo p" + big n: precompute factorials (`Comb`), never `math.comb` | `combinations.py` first try: 7 s per query |
| Integer geometry: cross product, no slopes or division | Point Location first try: floats + missed directions |
| Remove debug `print`s before submitting | Point Location: `print(slope)` |
| `sys.stdin.readline` gives `str`; `.buffer` gives bytes (only for all-number input) | |
| Greedy rule: try to break it with 3 tiny cases first | Movie Festival: almost sorted by length |
| Loop over **all** events/items: `range(len(x) - 1)` silently drops the last one | Restaurant Customers: only correct because the last event is a leave |
| 1000x1000 grid in Python: flat array, no allocation in the loop, PyPy | Labyrinth: correct but TLE |
| Range queries + anything that "looks back" (previous wizard, previous occurrence): the first element inside `[l, r]` needs special handling | PacNW K: first wizard in range |
| Counting inside each query range is O(n q). Many queries with a threshold: offline + Fenwick | PacNW K: too slow |
| `for i in t` where `t` is an int: use `range(t)`. `map(int, input())` needs `.split()` | `test.py` |
| Shortest path on a grid is **BFS** (queue), not DFS (stack). Store a parent per cell, walk back from the end | `labyrinth.py` |

## Proven: solved it myself

| Technique | Problems | Notebook page |
|---|---|---|
| Sort + greedy | CSES 1629 Movie Festival | techniques |
| Two pointers (same end and opposite ends) | CSES 1084 Apartments, 1090 Ferris Wheel (`n - pairs` trick), 1640 Sum of Two Values (sort `(value, index)` pairs) | techniques |
| Sweep line: +1 at start, -1 at end, sort events | CSES 1619 Restaurant Customers (7 min) | techniques: max_overlap |
| Cross product orientation | CSES 2189 Point Location Test | geometry |
| Fenwick tree (point set, range sum) | CSES 1648 | data structures |
| Sparse table (wrote my own, then fixed the bound) | CSES 1647 | data structures |
| nCr mod p with factorial tables | CSES 1079 | math |
| Fast I/O, building output with `join` | all of the above | template |

## Understood, not yet solid

Do one more problem of each type from a blank file before calling it proven.

| Technique | Where I saw it | Next problem |
|---|---|---|
| Range min + offline counting with Fenwick | PacNW K (idea right, too slow, too late) | rewrite K from a blank file |
| Sort + suffix max + bisect ("does some j beat i?") | PacNW I (upsolved with help) | CSES 1645 Nearest Smaller Values |
| BFS shortest path + path reconstruction | `labyrinth.py` (correct, TLE in Python) | resubmit 1193 with PyPy / flat array |
| Custom comparators (`cmp_to_key`) | notes | "largest number" ordering |
| Prefix sums, rhombus / row sums | Roblox OA | CSES 1646, 1652 |

## Not yet

DP (all of it), Dijkstra/DSU/topological sort in practice, trees and LCA, strings, flows, game theory. These follow the weekly plan in the Regionals Camp app.

## Contest record

| Contest | Result | Lessons |
|---|---|---|
| PacNW 2026 Div 1 (Nov 14) | Team: E only. I and J unsolved, A attempted. My K: right idea, no other team solved it, 3 min late | Easy problems decide placement; check the brute force on edge ranges; offline counting pattern |
