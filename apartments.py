import sys
input = sys.stdin.readline

def mno(i):
    cnt, last = 0, float('-inf')
    
    new_lst = []
    
    for s, e in sorted(i, key= lambda x: x[1]):
        if s >= last:
            cnt += 1
            last = e
            new_lst.append((s, e))
            
    return new_lst

n, a, diff = map(int, input().split())

'''4 3 5
60 45 80 60
30 60 75
isn't it just (55, 65)
55, 56, 57, 58, 59, 60, 65
'''

desired = sorted(list(map(int, input().split())))
weirdo_list = []
apartments = sorted(list(map(int, input().split())))

def two_sum_sorted(a, b, k):
    i, j =0, 0
    cnt = 0
    while i < len(a) and j < len(b):
        s =  b[j] - a[i] 
        if abs(s) <= k:
            cnt += 1
            i+=1
            j+=1
            continue
            
        if s < 0:
            j += 1
        elif s > 0:
            i += 1
    return cnt

print(two_sum_sorted(desired, apartments, diff))
    
    

    
    
