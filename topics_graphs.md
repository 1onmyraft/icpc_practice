# Graphs, including Dijkstra

Templates are in notebook/graphs.py (BFS, Dijkstra, DSU, topological sort).

## Order
1. Representation: adjacency lists, reading edges fast. Know 0-index vs 1-index.
2. BFS: shortest path in unweighted graphs, grid BFS, multi-source BFS, 0-1 BFS.
3. DFS: connected components, cycle detection, bipartite check. In Python use an
   iterative stack to avoid recursion limits.
4. Dijkstra: non-negative weights, heap, skip stale entries. Then:
   - Dijkstra on states (node, extra) such as (node, used coupon) for CSES Flight Discount
   - path reconstruction with a parent array
   - counting shortest paths (CSES Flight Routes Check and Investigation)
5. DSU: components, Kruskal MST, offline connectivity.
6. Topological sort and DAG DP (NAQ I was a flavour of this).
7. Floyd-Warshall for n <= ~400; Bellman-Ford for negative edges.
8. Later: bridges, SCC, LCA, flows.

## Dijkstra checklist
- Edge weights negative? Use Bellman-Ford.
- Weights only 0 and 1? Use 0-1 BFS with a deque.
- State bigger than a node? Put it in the tuple and the dist array.
- Large distances: Python ints are fine, C++ needs long long.

## Practice (CSES Graph Algorithms)
Counting Rooms, Labyrinth, Building Roads, Message Route, Round Trip,
Shortest Routes I, Flight Discount, Cycle Finding, Road Reparation, Planets and Kingdoms.
