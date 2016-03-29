from pythometry import Line
from pythometry import Polygon
import timeit


def run_timer(text, function):
    t = timeit.Timer("{function}()".format(function=function.__name__),
                     "from __main__ import {function}".format(function=function.__name__))
    tmpl = "%.2f usec/pass"
    print("-", text, "\t", tmpl % (1000000 * t.timeit(number=100000)/100000))

line1 = Line(0, 0, 100, 100)
line2 = Line(100, 0, 0, 100)
assert line1.touches(line2)
assert line1.findtouchpoint(line2) == (50, 50)

def crossed_lines_touch():
    line1.touches(line2)

def crossed_lines_touchpoint():
    line1.findtouchpoint(line2)

run_timer("Does two crossed lines touch? (yes)", crossed_lines_touch)
run_timer("Where does two crossed lines touch?", crossed_lines_touchpoint)

line1 = Line(0, 0, 100, 100)
line2 = Line(10, 10, 110, 110)
assert line1.touches(line2)
assert line1.findtouchpoint(line2) is not None

def lines_on_top_of_eachother_touch():
    line1.touches(line2)

def lines_on_top_of_eachother_touchpoint():
    line1.findtouchpoint(line2)

run_timer("Does two parallel lines on top of each other touch? (yes)", lines_on_top_of_eachother_touch)
run_timer("Where does two parallel lines on top of each other touch?", lines_on_top_of_eachother_touchpoint)

line1 = Line(0, 0, 100, 100)
line2 = Line(10, 0, 110, 100)
assert not line1.touches(line2)

def lines_close_but_not_touching_touch():
    line1.touches(line2)

def lines_close_but_not_touching_touchpoint():
    line1.findtouchpoint(line2)

run_timer("Does two non overlapping parallel lines touch? (no, but close)", lines_close_but_not_touching_touch)
run_timer("Where does two non overlapping parallel lines touch?", lines_close_but_not_touching_touchpoint)

line1 = Line(0, 0, 100, 100)
line2 = Line(210, 210, 310, 310)
assert not line1.touches(line2)

def lines_far_away_touch():
    line1.touches(line2)

def lines_far_away_touchpoint():
    line1.findtouchpoint(line2)

run_timer("Does two lines far away from each other touch? (no)", lines_far_away_touch)
run_timer("Does two lines far away from each other touch? (no)", lines_far_away_touchpoint)

diamond = Polygon([(-100, 0), (0, -100), (100, 0), (0, 100)])
square = Polygon([(-75, -75), (75, -75), (75, 75), (-75, 75)])

def nestled_polygons_touch():
    diamond.touches(square)

run_timer("Does two polygons nestled on each other touch? (yes)", nestled_polygons_touch)

def nestled_polygons_enclose():
    diamond.encloses(square)

run_timer("Does two polygons nestled on each other enclose? (no)", nestled_polygons_enclose)

bigdiamond = Polygon([(-200, 0), (0, -200), (200, 0), (0, 200)], close=True)
tinysquare = Polygon([(-5, -5), (5, -5), (5, 5), (-5, 5)], close=True)

def bigdiamond_enclose_tinysquare():
    bigdiamond.encloses(tinysquare)

run_timer("Does a big polygon enclose a small one? (yes)", bigdiamond_enclose_tinysquare)
