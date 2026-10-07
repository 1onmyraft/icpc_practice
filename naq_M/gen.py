import random


def random_case(n, max_val=4, seed=None):
    """Connected graph with n vertices and n edges (one cycle), n >= 3."""
    rng = random.Random(seed)
    edges = []
    for v in range(1, n):                  # random tree
        edges.append((rng.randrange(v), v))
    while True:                            # one extra edge makes the cycle
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and (a, b) not in edges and (b, a) not in edges:
            edges.append((a, b))
            break
    vals = [rng.randint(0, max_val) for _ in range(n)]
    k = rng.randint(0, max_val)
    return n, k, vals, edges
