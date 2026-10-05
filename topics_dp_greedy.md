# DP and greedy: a method, then drills

## Why DP feels hard
You solve problems by reasoning forward. DP asks you to define a *state* first.
Fix: for every problem ask these four questions in order.
1. What is the smallest description of "where I am"? (index i, remaining capacity, mask, last choice)
2. What do I want to know about that state? (best value, count, true/false)
3. How does a state depend on smaller states? (the recurrence)
4. What are the base cases and the answer state?

Write the recurrence in a comment BEFORE coding. Start with brute-force recursion plus
`functools.lru_cache`, then convert to a table only if too slow.

## DP ladder (do in order, about 2 problems each)
1. 1D: climbing stairs, coin change (min coins), coin combinations (count), house robber
2. Knapsack: 0/1 knapsack, unbounded knapsack, subset sum
3. Sequences: LIS (O(n log n) with bisect), LCS, edit distance
4. Grid: grid paths with obstacles, min path sum
5. Intervals: matrix chain style, palindromic substrings
6. Bitmask: TSP in O(n^2 2^n), assignment problems
7. Trees: subtree sizes, max independent set, diameter
8. Digit DP and SOS DP (later, only if time allows)

Good problem sources: CSES Problem Set "Dynamic Programming" section
(Dice Combinations, Minimizing Coins, Coin Combinations I/II, Grid Paths, Book Shop,
Array Description, Edit Distance, Longest Common Subsequence, Elevator Rides).

## Greedy: how to trust it
A greedy works only if you can state why. Check one of:
- Exchange argument: swapping adjacent items never helps.
- "Stays ahead": after each step, greedy is at least as good as any other.
- Matroid-like structure (rare).
If you cannot argue it in two sentences, test it against brute force on small inputs.

Core greedy patterns (do 2 problems each):
1. Sort by end time: interval scheduling (CSES Movie Festival)
2. Sort then pair: two pointers (CSES Ferris Wheel)
3. Heap-based greedy: scheduling with deadlines (CSES Tasks and Deadlines), Huffman-style merging
4. Binary search on the answer: "min X such that feasible" (CSES Factory Machines)
5. Sweep line: sort events (CSES Restaurant Customers)

## Stress-test habit
Write a slow brute force, generate random small cases, compare. This catches wrong
greedies fast, and your analytical skills make you good at the brute force.
