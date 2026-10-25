# 2021 ICPC North America Regionals (your Oct 24 practice set)

Ordered by Kattis difficulty. "Tested" means the solution passes the Kattis samples
and matches a brute force on random small inputs (not run on the Kattis judge).

| Problem | Kattis | Diff | Your team | Technique | Recognition trigger | Solution |
|---|---|---|---|---|---|---|
| K Tournament Seeding | tournamentseeding | 3.8 | AC (9 tries) | recursion / greedy by rounds | power-of-two bracket, "top 2^r must reach round r" | yours |
| F Rise and Fall | riseandfall | 4.4 | AC (5 tries) | greedy on digits | "largest number <= n with property", 10^5 digits | yours |
| H Reversibly Cyclic Strings | (not found on Kattis) | – | AC (2 tries) | – | – | yours |
| A Circle Bounce | circlebounce | 4.8 | – | complex numbers as rotations + fast power mod p | reflections in a circle, huge n, answer mod p | circlebounce.py (tested) |
| E Problem Set Construction | problemsetconstruction | 5.2 | – | probability DP (knapsack over time) | "probability it gets solved", n <= 50, t <= 2500 | idea below |
| M Tree Hopping | treehopping | 5.4 | – | BFS parent/depth, climb at most 3 steps | "distance <= small constant" in a tree | treehopping.py (tested) |
| B Shortest Missing Subsequences | shortestmissingsubsequences | 5.5 | – | greedy blocks + bisect on positions | subsequence, "shortest string NOT contained" | shortestmissingsubsequences.py (tested) |
| L Dorm Room Divide | dormroomdivide | 5.8 | – | fan triangulation + prefix areas | split convex polygon area from a vertex | dormroomdivide.py (tested) |
| I Diagonals | diagonals | 6.4 | – | backtracking + DSU loop check | n <= 8 puzzle, "no loops" | idea below |
| C XOR Island | xorisland | 6.5 | – | logic puzzle (common knowledge) | islanders / hats / "who knows when" | skip for now |
| D Archery Accuracy | archeryaccuracy | 6.8 | – | bitmask DP + gambler's ruin | n <= 17 ordering choice, random walk to +-s | idea below |
| G Hopscotch 500 | hopscotch500 | 7.0 | – | layered DP, min() splits into row and column | distance = min(dr, dc)^2, numbers 1..k in order | hopscotch500.cpp (tested) |
| J Fail Them All! | failthemall | 7.5 | – | 2-SAT, lexicographically smallest | "at most one of each pair true", T/F choices | idea below |

## Drill order
1. Circle Bounce, Tree Hopping, Shortest Missing Subsequences: read the file's top comment,
   close it, write it yourself, submit on Kattis.
2. Dorm Room Divide, Hopscotch 500: same.
3. Stretch: Problem Set Construction, Fail Them All, Archery Accuracy, Diagonals (ideas below).

## Ideas for the ones without a solution file (not yet verified)
- **Problem Set Construction.** Teams take the solvable problems with the smallest times
  first, so problem i is solved iff it is solvable and its time plus the times of the
  solvable chosen problems faster than it fits in t. Sort by time; DP over the faster
  problems on (how many chosen, total time of the solvable ones); problems slower than i
  only matter through how many of them are chosen (a binomial coefficient).
- **Fail Them All!** One boolean per question. A student fails iff no two of their answered
  questions are both correct, so for every pair of a student's answers add the clause
  "not both correct". That is 2-SAT. For the lexicographically smallest key, fix questions
  left to right to F if the formula stays satisfiable, otherwise T.
- **Archery Accuracy.** After each round the score is exactly +s or -s. Choosing the order
  of n <= 17 shooters is a bitmask DP: dp[set of shooters used][sign of score]. Moving from
  +-s_prev to +-s_next is a random walk with absorbing ends: the gambler's ruin formula.
- **Diagonals.** Fill cells one at a time with / or \. Prune when an intersection's count
  can no longer be met. Keep a DSU over grid corners: a diagonal joins two corners, and if
  they are already connected the new diagonal closes a loop.

## From brute force to the algorithm
You said you brute force everything. That is the right first step: almost every standard
algorithm is a brute force with the repeated work removed. Ask, in order:
1. What is the brute force? (Write it, even if only in your head.)
2. What does it repeat, or what does it compute that it never needs?
3. What structure removes that?

How that went in this set:
- **Tree Hopping:** brute force = BFS for every pair. Unneeded work: exact distances, when
  only "is it <= 3?" matters. Fix: climb parents, stop after 3 steps.
- **Shortest Missing Subsequences:** brute force = try every string of length 1, 2, 3...
  Repeated work: re-scanning s for every candidate. Fix: the greedy blocks give the length
  directly; bisect makes each subsequence check fast.
- **Hopscotch 500:** brute force = every tile of layer t to every tile of layer t+1.
  Repeated work: the min() means a hop only depends on the row OR the column, so pairs of
  tiles are never needed. Fix: per-row and per-column best values.
- **Circle Bounce:** brute force = simulate each bounce. Repeated work: every bounce is the
  same rotation. Fix: repeated multiplication = fast exponentiation.
