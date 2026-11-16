import math
import sys

input = sys.stdin.readline


n = int(input().strip())


import sys
input = sys.stdin.readline
MOD = 10**9 + 7

# ---- copied from notebook: Math -> Comb ----
class Comb:
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
# --------------------------------------


arb = Comb(10**6)
output = []
for i in range(n):
    a, b = map(int, input().split())
    
    output.append(arb.C(a, b))
    
print('\n'.join(map(str, output)))