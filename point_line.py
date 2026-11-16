import sys

input = sys.stdin.buffer.readline


num_tests = int(input())

def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

output = []
for test in range(num_tests):
    x1, y1, x2, y2, x3, y3 = map(int, input().split())
    
    
    
    
    johnson = (cross((x1, y1), (x2, y2), (x3, y3)))
    
    
    if johnson > 0:
        output.append('LEFT') 
    elif johnson < 0:
        output.append('RIGHT')
    else:
        output.append('TOUCH')
    

print('\n'.join(output))

# point slope form:
# y-y1 = m(x-x1)
#y-y1 = mx-mx1
#y-y1-mx = -mx1
# -y+y1+mx = mx1
#-y/m +y1/m + x = x1