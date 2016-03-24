from pythometry import Line
from pythometry import Polygon
import timeit


line1 = Line(0, 0, 100, 100)
line2 = Line(100, 0, 0, 100)
assert line1.touches(line2)

def intersection():
    line1.touches(line2)

t = timeit.Timer("intersection()", "from __main__ import intersection")
print("Line Intersection: %.2f usec/pass" % (1000000 * t.timeit(number=100000)/100000))


line1 = Line(0, 0, 100, 100)
line2 = Line(10, 10, 110, 110)
assert line1.touches(line2)

def shifted():
    line1.touches(line2)

t = timeit.Timer("shifted()", "from __main__ import shifted")
print("Shifted lines: %.2f usec/pass" % (1000000 * t.timeit(number=100000)/100000))


line1 = Line(0, 0, 100, 100)
line2 = Line(10, 0, 110, 100)
assert not line1.touches(line2)

def non_intersection():
    line1.touches(line2)

t = timeit.Timer("non_intersection()", "from __main__ import non_intersection")
print("Line Non Intersection: %.2f usec/pass" % (1000000 * t.timeit(number=100000)/100000))


line1 = Line(0, 0, 100, 100)
line2 = Line(210, 210, 310, 310)
assert not line1.touches(line2)

def non_overlapping():
    line1.touches(line2)

t = timeit.Timer("non_overlapping()", "from __main__ import non_overlapping")
print("Line Non Overlappling: %.2f usec/pass" % (1000000 * t.timeit(number=100000)/100000))


diamond = Polygon([(-100, 0), (0, -100), (100, 0), (0, 100)])
square = Polygon([(-75, -75), (75, -75), (75, 75), (-75, 75)])
assert not line1.touches(line2)

def polygon():
    diamond.touches(square)

t = timeit.Timer("polygon()", "from __main__ import polygon")
print("Polygon Intersecting: %.2f usec/pass" % (1000000 * t.timeit(number=100000)/100000))
