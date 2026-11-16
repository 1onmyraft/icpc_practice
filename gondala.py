import sys
from functools import cmp_to_key

def two_sum_sorted(a , k):
    i, j =0, len(a)-1
    cnt = 0
    while i < j:
        s =  a[i] + a[j]
        if s <= k:
            i += 1
            j -= 1
            cnt += 1
        else:
            j -= 1
        
    return cnt

input = sys.stdin.readline


n, x = map(int, input().split())

weights = sorted(map(int, input().split()))


print(n-two_sum_sorted(weights, x))
