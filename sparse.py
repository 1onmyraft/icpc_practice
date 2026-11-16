import math
import sys

input = sys.stdin.readline


n, q = map(int, input().split())

array = list(map(int, input().split()))

    


test_arr = array


arr_len = len(test_arr)

sparse = [[float('inf') for _ in range(arr_len)] for _ in  range(int(math.log(arr_len, 2))+ 1)]




for i in range(len(sparse)):
    for j in range(len(sparse[0])):
        if i == 0:
            sparse[i][j] = test_arr[j]
        else:
            if j+ pow(2, i) <= len(sparse[0]):
                sparse[i][j] = min(sparse[i-1][j], sparse[i-1][j+ pow(2, i-1)] )
            
            

def get_range(start, end):
    diff = end-start+1
    max_pow = int(math.log(diff, 2))
        
    return min(sparse[max_pow][start], sparse[max_pow][end-pow(2, max_pow)+1])


output = []
for i in range(q):
    start, end = map(int, input().split())
    
    output.append(str(get_range(start-1, end-1)))
    
    
print('\n'.join(output))
    
        
        
            