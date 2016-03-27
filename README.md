# pythometry
A humble library for doing shape intersection

## Background
I needed a library for another project that does line intersection and some other basic geometrical calculations.
I could not find a library that did this without complicated licensing or 3rd party dependencies of several hundred
megabytes.
It all felt too overkill, so I thought I would try to fill the gap with this open source project.

## Mission
It is pythometrys mission to be an available, easy to distribute, publicly licensed geometrical library for python.
The mission parameters does not allow reliance third party library dependence. However, third party libraries may be
added for reasons to speed up calculations. However all functionality must work without it.

## Compatibility
Only tested on:
- Python 3.4 64-bit


## Current benchmarks:
- Does two crossed lines touch? (yes) 	 17.13 usec/pass
- Where does two crossed lines touch? 	 20.70 usec/pass
- Does two parallel lines on top of each other touch? (yes) 	 4.15 usec/pass
- Where does two parallel lines on top of each other touch? 	 4.14 usec/pass
- Does two non overlapping parallel lines touch? (no, but close) 	 5.99 usec/pass
- Where does two non overlapping parallel lines touch? 	 5.99 usec/pass
- Does two lines far away from each other touch? (no) 	 0.84 usec/pass
- Does two lines far away from each other touch? (no) 	 0.85 usec/pass
- Does two polygons nestled on each other touch? (yes) 	 21.09 usec/pass

