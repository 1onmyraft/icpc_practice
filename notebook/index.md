# Contest index: look up by constraint or phrase (fits on one page)

## Constraints -> what complexity you can afford
| n | Allowed | Think |
|---|---|---|
| <= 10-12 | O(n!) | permutations, brute force |
| <= 20-25 | O(2^n * n) | bitmask DP, subsets, meet in the middle (n up to 40) |
| <= 400-500 | O(n^3) | Floyd-Warshall, interval DP |
| <= 5,000 | O(n^2) | 2D DP, all pairs |
| <= 1e5-2e5 | O(n log n) | sort, heap, segment tree, binary search, Dijkstra |
| <= 1e6 | O(n) or O(n log n) | sieve, linear scan, two pointers |
| <= 1e9 | O(sqrt n) or O(log n) | math, divisor loops |
| <= 1e18 | O(log n) or formula | closed form, binary search on the answer, fast exponentiation |

Python does roughly 1e7 simple steps per second. If it is too slow, switch to C++.

## Phrase -> technique
| The statement says | Try |
|---|---|
| shortest path, minimum cost to travel | BFS (unit), 0-1 BFS, Dijkstra (nonneg), Bellman-Ford (negative) |
| connected, merge groups, same component | DSU |
| order, before/after, dependencies, prerequisites | topological sort |
| minimum X such that ... is possible | binary search on the answer |
| number of ways, modulo 998244353 | DP or combinatorics (factorials, inverses) |
| maximum number of non-overlapping | greedy by end time |
| minimum number of operations | BFS over states, greedy, or DP |
| k-th smallest / largest | sort, heap, binary search |
| range sum / range min with updates | Fenwick, segment tree, sparse table (no updates) |
| next greater / smaller element | monotonic stack |
| substring, pattern, prefix | KMP, Z, hashing, trie |
| convex, farthest points, polygon area | cross product, hull, rotating calipers |
| every pair of vertices, tree | rerooting, LCA, centroid, counting by edges |
| grid, paths right/down | DP |
| game, both play optimally | Sprague-Grundy, minimax DP, parity |
| interactive | flush after each print, randomization |
| exactly one cycle (n vertices, n edges) | peel leaves, hanging trees |
| minimize sum of squares / convex cost | Cauchy-Schwarz, Lagrange, ternary search |

## Traps to check before submitting
- multiple test cases: reset everything per case
- overflow (C++ long long), modulo applied after every multiply
- 0-index vs 1-index
- scanning a list when you should use a set or dict
- recursion depth in Python (use an iterative stack or raise the limit)
- printing floats with a fixed number of decimals
- ordered vs unordered pairs, k = 0, n = 1 edge cases
- test the sample and one tiny edge case before submitting
