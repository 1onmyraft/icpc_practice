# NAQ 2026 post-mortem

Started about 90 min late. Result: A partial (0.4), B, E, F, H, J, K solved. I attempted.
C, D, G, L, M not attempted.

| Problem | Technique | Status |
|---|---|---|
| A | n(n+1)(n+2)/6 mod p; reduce before multiplying | partial, find the cause |
| B | difference of consecutive differences | solved |
| C | sort by area, count placements, k! for congruent | todo |
| D | convex hull, rotating calipers, diameters | todo |
| E | antidiagonal construction | solved |
| F | bucket = (x-1)//10 in a set | solved |
| G | second map of value counts | todo, easy |
| H | interactive, random first guess, certain second | solved |
| I | any a>b means -1, else count missing (i,i+1); use a set | fix in solutions/ |
| J | print 's' + 'h'*(n+1) | solved |
| K | only 45 valid numbers, binary search | solved |
| L | answer p^2 / sum(t) | todo, easy |
| M | one cycle plus hanging trees, count pairs and double | todo |

## Lessons
- Read all problems first and rank by difficulty.
- Use sets and dicts instead of list membership tests.
- Use sys.stdin for large input.
- Several unattempted problems were easy once the technique is known.
