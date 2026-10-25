# Dorm Room Divide (Kattis dormroomdivide, difficulty 5.8)
# Idea: fan-triangulate from the door (vertex 0): triangles (0, i, i+1). Walk the
# triangles adding area until the running total would pass half. The cut ends on
# edge (i, i+1) at fraction t, and the area of triangle (0, i, point) grows linearly
# in t, so t = remaining / triangle_area. Use exact integer cross products (twice
# the area) so nothing is lost before the final division.
import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(x) for x in data[1:2 * n + 1:2]]
    ys = [int(y) for y in data[2:2 * n + 2:2]]
    x0, y0 = xs[0], ys[0]

    def tri2(i):  # twice the area of triangle (0, i, i+1), positive for CCW input
        return (xs[i] - x0) * (ys[i + 1] - y0) - (ys[i] - y0) * (xs[i + 1] - x0)

    total2 = sum(tri2(i) for i in range(1, n - 1))
    half2 = total2 / 2          # target, in "twice the area" units
    acc = 0
    for i in range(1, n - 1):
        a = tri2(i)
        if acc + a >= half2:
            t = (half2 - acc) / a
            px = xs[i] + t * (xs[i + 1] - xs[i])
            py = ys[i] + t * (ys[i + 1] - ys[i])
            print("%.9f %.9f" % (px, py))
            return
        acc += a

main()
