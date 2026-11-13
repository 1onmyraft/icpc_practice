"""Math page: number theory, combinatorics, binary search. Self-test: python3 math_nt.py

SPOT IT
  "modulo 1e9+7 / 998244353"   -> work mod p the whole time, divide = multiply by inverse
  "number of ways to choose"   -> nCr with factorial tables
  "gcd/lcm/divisible"          -> gcd, sieve, factorize
  "a^b with huge b"            -> pow(a, b, m)   (built in, fast)
  "minimum X such that ok(X)"  -> binary search on the answer (ok must be monotone)
  "a*x + b*y = c"              -> extended gcd
  "x = r1 mod m1, x = r2 mod m2" -> CRT
Python ints never overflow; math.isqrt(n) is the exact integer sqrt; math.comb(n,k) exact.
"""
from math import gcd, isqrt

MOD = 10**9 + 7


def lcm(a, b):
    return a // gcd(a, b) * b


def ext_gcd(a, b):
    """returns (g, x, y) with a*x + b*y = g = gcd(a, b)"""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def modinv(a, m=MOD):
    """m prime: pow(a, m-2, m).  General m (gcd(a,m)=1): pow(a, -1, m) in Python 3.8+"""
    return pow(a, -1, m)


def crt(r1, m1, r2, m2):
    """x = r1 (mod m1), x = r2 (mod m2). Returns (x, lcm) or None if impossible."""
    g, p, _ = ext_gcd(m1, m2)
    if (r2 - r1) % g:
        return None
    l = m1 // g * m2
    x = (r1 + (r2 - r1) // g * p % (m2 // g) * m1) % l
    return x, l


def sieve(n):
    """is_p[i] for 0..n, and list of primes. O(n log log n). n up to ~1e7 in PyPy."""
    is_p = bytearray([1]) * (n + 1)
    is_p[0:2] = b'\x00\x00'[:min(2, n + 1)]
    for i in range(2, isqrt(n) + 1):
        if is_p[i]:
            is_p[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    return is_p, [i for i in range(n + 1) if is_p[i]]


def spf_sieve(n):
    """smallest prime factor for 0..n -> factorize any x <= n in O(log x)"""
    spf = list(range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def factorize(n):
    """trial division, O(sqrt n). Returns {prime: exponent}"""
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors(n):
    small, large, d = [], [], 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)
        d += 1
    return small + large[::-1]


def phi(n):
    """Euler totient: count of 1..n coprime to n"""
    r = n
    for p in factorize(n):
        r -= r // p
    return r


class Comb:
    """nCr mod p (p prime, n < p) in O(1) after O(N) precompute."""
    def __init__(self, N, p=MOD):
        self.p = p
        f = [1] * (N + 1)
        for i in range(1, N + 1):
            f[i] = f[i - 1] * i % p
        inv = [1] * (N + 1)
        inv[N] = pow(f[N], p - 2, p)
        for i in range(N, 0, -1):
            inv[i - 1] = inv[i] * i % p
        self.f, self.inv = f, inv

    def C(self, n, k):
        if k < 0 or k > n:
            return 0
        return self.f[n] * self.inv[k] % self.p * self.inv[n - k] % self.p

    def P(self, n, k):          # ordered selections
        if k < 0 or k > n:
            return 0
        return self.f[n] * self.inv[n - k] % self.p
# stars and bars: ways to split n identical items into k groups (>=0 each) = C(n+k-1, k-1)
# Catalan(n) = C(2n, n) / (n+1)   (balanced parens, binary trees, non-crossing)
# inclusion-exclusion: |A or B| = |A| + |B| - |A and B|; over subsets with sign (-1)^|S|


def mat_mul(A, B, m=MOD):
    n, k, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        Ai, Ci = A[i], C[i]
        for t in range(k):
            a = Ai[t]
            if a:
                Bt = B[t]
                for j in range(p):
                    Ci[j] += a * Bt[j]
        for j in range(p):
            Ci[j] %= m
    return C


def mat_pow(A, e, m=MOD):
    """linear recurrences in O(k^3 log e): fib(n) = mat_pow([[1,1],[1,0]], n)[0][1]"""
    n = len(A)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    while e:
        if e & 1:
            R = mat_mul(R, A, m)
        A = mat_mul(A, A, m)
        e >>= 1
    return R


# ---------- binary search ----------
def first_true(lo, hi, ok):
    """smallest x in [lo, hi] with ok(x) True; ok must be F..F T..T. Returns hi+1 if none."""
    hi += 1
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def last_true(lo, hi, ok):
    """largest x in [lo, hi] with ok(x) True; ok must be T..T F..F. Returns lo-1 if none."""
    lo -= 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def bsearch_real(lo, hi, ok, iters=100):
    """real-valued: smallest x with ok(x). 100 iterations is always enough."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


def ternary_max(lo, hi, f, iters=200):
    """max of a unimodal (up then down) real function on [lo, hi]"""
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    return (lo + hi) / 2


if __name__ == "__main__":
    import random
    from math import comb
    for _ in range(2000):
        a, b = random.randint(1, 10**6), random.randint(1, 10**6)
        g, x, y = ext_gcd(a, b)
        assert g == gcd(a, b) and a * x + b * y == g
        assert lcm(a, b) % a == 0 and lcm(a, b) % b == 0 and lcm(a, b) == a * b // g
        m1, m2 = random.randint(1, 60), random.randint(1, 60)
        r1, r2 = random.randrange(m1), random.randrange(m2)
        res = crt(r1, m1, r2, m2)
        brute = [x for x in range(lcm(m1, m2)) if x % m1 == r1 and x % m2 == r2]
        assert (res is None) == (not brute)
        if res:
            assert res == (brute[0], lcm(m1, m2))
    for n in range(0, 300):
        is_p, ps = sieve(n)
        exp = [i for i in range(n + 1) if i >= 2 and all(i % d for d in range(2, i))]
        assert ps == exp
    spf = spf_sieve(5000)
    for n in range(1, 5000):
        f = factorize(n)
        prod = 1
        for p, e in f.items():
            prod *= p ** e
        assert prod == n
        x, g2 = n, {}
        while x > 1:
            g2[spf[x]] = g2.get(spf[x], 0) + 1
            x //= spf[x]
        assert g2 == f
        assert divisors(n) == [d for d in range(1, n + 1) if n % d == 0]
        if n < 600:
            assert phi(n) == sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)
    assert modinv(3) * 3 % MOD == 1
    cb = Comb(500)
    for n in range(60):
        for k in range(-1, 62):
            assert cb.C(n, k) == (comb(n, k) % MOD if 0 <= k <= n else 0)
    fib = [0, 1]
    for _ in range(100):
        fib.append(fib[-1] + fib[-2])
    for n in range(1, 90):
        assert mat_pow([[1, 1], [1, 0]], n, 10**30)[0][1] == fib[n]
    for _ in range(500):
        t = random.randint(-50, 50)
        assert first_true(-40, 40, lambda x: x >= t) == (min(max(t, -40), 41))
        assert last_true(-40, 40, lambda x: x <= t) == (max(min(t, 40), -41))
    assert abs(bsearch_real(0, 10, lambda x: x * x >= 2) - 2 ** 0.5) < 1e-9
    assert abs(ternary_max(-10, 10, lambda x: -(x - 3.3) ** 2) - 3.3) < 1e-6
    print("math_nt: all tests passed")
