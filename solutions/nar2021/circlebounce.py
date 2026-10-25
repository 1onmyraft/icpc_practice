# Circle Bounce (Kattis circlebounce, 2021 NA Regionals, difficulty 4.8)
# Idea: every bounce rotates the strike point by the same angle. Write points as
# complex numbers: start P0 = -1, first strike P1 = ((b^2-a^2) + 2ab i)/(a^2+b^2),
# rotation w = P1 / P0 = -P1, so strike k is P0 * w^k = -(w^k).
# n bounces -> strike number n+1. Do complex multiplication mod p with fast power.
import sys

P = 10**9 + 7

def mul(x, y):
    return ((x[0] * y[0] - x[1] * y[1]) % P, (x[0] * y[1] + x[1] * y[0]) % P)

def cpow(z, e):
    r = (1, 0)
    while e:
        if e & 1:
            r = mul(r, z)
        z = mul(z, z)
        e >>= 1
    return r

def main():
    a, b, n = map(int, sys.stdin.read().split())
    inv = pow(a * a + b * b, P - 2, P)
    p1 = ((b * b - a * a) * inv % P, 2 * a * b * inv % P)
    w = (-p1[0] % P, -p1[1] % P)
    pk = cpow(w, n + 1)
    print(-pk[0] % P)

main()
