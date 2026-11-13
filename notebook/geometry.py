"""Geometry page. Points are tuples (x, y). Self-test: python3 geometry.py

RULES
  * Integer input -> stay in integers (cross products, squared distances). No floats, no sqrt.
  * Floats only when forced (circles, angles); compare with EPS = 1e-9.
  * cross(o, a, b) > 0: o->a->b turns LEFT (counter-clockwise); < 0 right; = 0 collinear.
  * Polygon area = |shoelace| / 2; 2*area is an integer for integer points.
  * Pick's theorem: Area = I + B/2 - 1  (I interior lattice pts, B boundary lattice pts)
  * boundary lattice points on segment = gcd(|dx|, |dy|)  (excluding one endpoint)
  * angle of a vector: math.atan2(y, x) in (-pi, pi];  math.hypot(dx, dy) = length
"""
from math import gcd, hypot, sqrt, atan2

EPS = 1e-9


def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def cross2(a, b): return a[0] * b[1] - a[1] * b[0]
def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
def dist2(a, b): return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def sign(x):
    return (x > EPS) - (x < -EPS)


def on_segment(p, a, b):
    """p on closed segment ab (exact for ints)"""
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def seg_intersect(a, b, c, d):
    """do closed segments ab and cd touch/cross? (exact for ints)"""
    d1, d2 = cross(a, b, c), cross(a, b, d)
    d3, d4 = cross(c, d, a), cross(c, d, b)
    if ((d1 > 0) != (d2 > 0)) and d1 != 0 and d2 != 0 and \
       ((d3 > 0) != (d4 > 0)) and d3 != 0 and d4 != 0:
        return True
    return on_segment(c, a, b) or on_segment(d, a, b) or on_segment(a, c, d) or on_segment(b, c, d)


def line_intersection(a, b, c, d):
    """intersection point of infinite lines ab and cd (floats), None if parallel"""
    r, s = sub(b, a), sub(d, c)
    den = cross2(r, s)
    if den == 0:
        return None
    t = cross2(sub(c, a), s) / den
    return (a[0] + t * r[0], a[1] + t * r[1])


def point_seg_dist(p, a, b):
    ab, ap = sub(b, a), sub(p, a)
    L = dot(ab, ab)
    if L == 0:
        return sqrt(dist2(p, a))
    t = max(0.0, min(1.0, dot(ap, ab) / L))
    return hypot(a[0] + t * ab[0] - p[0], a[1] + t * ab[1] - p[1])


def area2(poly):
    """twice the signed area (positive if counter-clockwise). Shoelace."""
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s


def point_in_polygon(p, poly):
    """1 inside, 0 on boundary, -1 outside. Any simple polygon. Exact for ints."""
    n, inside = len(poly), False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_segment(p, a, b):
            return 0
        if (a[1] > p[1]) != (b[1] > p[1]):
            # x-coordinate of crossing compared without division
            c = cross(a, b, p)
            if (c > 0) == (b[1] > a[1]):
                inside = not inside
    return 1 if inside else -1


def convex_hull(pts):
    """Andrew's monotone chain. Returns hull counter-clockwise, no collinear points.
    To KEEP collinear boundary points change both <= 0 to < 0 (careful with all-collinear)."""
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def diameter2(pts):
    """max squared distance between any two points: rotating calipers on the hull"""
    h = convex_hull(pts)
    n = len(h)
    if n == 1:
        return 0
    if n == 2:
        return dist2(h[0], h[1])
    best, j = 0, 1
    for i in range(n):
        ni = (i + 1) % n
        while abs(cross(h[i], h[ni], h[(j + 1) % n])) > abs(cross(h[i], h[ni], h[j])):
            j = (j + 1) % n
        best = max(best, dist2(h[i], h[j]), dist2(h[ni], h[j]))
    return best


def lattice_boundary(poly):
    return sum(gcd(abs(poly[i][0] - poly[i - 1][0]), abs(poly[i][1] - poly[i - 1][1]))
               for i in range(len(poly)))


def lattice_interior(poly):
    """Pick: I = A - B/2 + 1  ->  2I = 2A - B + 2"""
    return (abs(area2(poly)) - lattice_boundary(poly) + 2) // 2


def circle_line(c, r, a, b):
    """intersections of circle (center c, radius r) with line ab, as float points"""
    d = sub(b, a)
    f = sub(a, c)
    A, B, C = dot(d, d), 2 * dot(f, d), dot(f, f) - r * r
    disc = B * B - 4 * A * C
    if disc < -EPS:
        return []
    disc = sqrt(max(0.0, disc))
    ts = {(-B - disc) / (2 * A), (-B + disc) / (2 * A)}
    return [(a[0] + t * d[0], a[1] + t * d[1]) for t in sorted(ts)]


def closest_pair2(pts):
    """min squared distance, O(n log n) sweep. pts: list of tuples (len >= 2)."""
    import bisect
    pts = sorted(pts)
    best = dist2(pts[0], pts[1])
    active, left = [], 0          # active sorted by (y, x)
    for p in pts:
        while (p[0] - pts[left][0]) ** 2 > best:
            q = pts[left]
            active.pop(bisect.bisect_left(active, (q[1], q[0])))
            left += 1
        d = int(sqrt(best)) + 1
        lo = bisect.bisect_left(active, (p[1] - d, -10**18))
        hi = bisect.bisect_right(active, (p[1] + d, 10**18))
        for y, x in active[lo:hi]:
            best = min(best, dist2(p, (x, y)))
        bisect.insort(active, (p[1], p[0]))
    return best


if __name__ == "__main__":
    import random
    R = lambda: random.randint(-6, 6)
    for _ in range(3000):
        a, b, c, d = [(R(), R()) for _ in range(4)]
        # brute: sample segment points on a fine rational grid via parametric check
        def brute(a, b, c, d):
            from fractions import Fraction as F
            r, s = sub(b, a), sub(d, c)
            den = cross2(r, s)
            if den != 0:
                t = F(cross2(sub(c, a), s), den)
                u = F(cross2(sub(c, a), r), den)
                return 0 <= t <= 1 and 0 <= u <= 1
            if cross(a, b, c) != 0:
                return False
            return on_segment(c, a, b) or on_segment(d, a, b) or on_segment(a, c, d) or on_segment(b, c, d)
        assert seg_intersect(a, b, c, d) == brute(a, b, c, d), (a, b, c, d)
    for _ in range(300):
        pts = [(R(), R()) for _ in range(random.randint(1, 12))]
        h = convex_hull(pts)
        for p in set(pts):        # every point inside or on hull
            if len(h) >= 3:
                assert point_in_polygon(p, h) >= 0
        for i in range(len(h)):   # strictly convex, ccw
            if len(h) >= 3:
                assert cross(h[i], h[(i + 1) % len(h)], h[(i + 2) % len(h)]) > 0
        if len(pts) >= 2:
            bd = max(dist2(p, q) for p in pts for q in pts)
            assert diameter2(pts) == bd
            bc = min(dist2(pts[i], pts[j]) for i in range(len(pts)) for j in range(i + 1, len(pts)))
            assert closest_pair2(pts) == bc
        if len(h) >= 3:
            I = sum(1 for x in range(-7, 8) for y in range(-7, 8) if point_in_polygon((x, y), h) == 1)
            B = sum(1 for x in range(-7, 8) for y in range(-7, 8) if point_in_polygon((x, y), h) == 0)
            assert lattice_interior(h) == I and lattice_boundary(h) == B
    sq = [(0, 0), (4, 0), (4, 4), (0, 4)]
    assert area2(sq) == 32 and point_in_polygon((2, 2), sq) == 1 and point_in_polygon((4, 1), sq) == 0
    assert point_in_polygon((5, 1), sq) == -1
    L = [(0, 0), (6, 0), (6, 2), (2, 2), (2, 6), (0, 6)]    # non-convex L shape
    assert point_in_polygon((4, 4), L) == -1 and point_in_polygon((1, 5), L) == 1
    assert line_intersection((0, 0), (2, 2), (0, 2), (2, 0)) == (1.0, 1.0)
    assert abs(point_seg_dist((0, 3), (-1, 0), (1, 0)) - 3) < EPS
    pts = circle_line((0, 0), 5, (-10, 3), (10, 3))
    assert len(pts) == 2 and all(abs(hypot(*p) - 5) < 1e-9 for p in pts)
    assert len(circle_line((0, 0), 1, (-1, 1), (1, 1))) == 1
    print("geometry: all tests passed")
