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
- Does two crossed lines touch? (yes) 	 11.2512 microseconds/pass
- Where does two crossed lines touch? 	 10.4303 microseconds/pass
- Does two parallel lines on top of each other touch? (yes) 	 6.7589 microseconds/pass
- Where does two parallel lines on top of each other touch? 	 6.3586 microseconds/pass
- Does two non overlapping parallel lines touch? (no, but close) 	 8.3299 microseconds/pass
- Where does two non overlapping parallel lines touch? 	 8.1699 microseconds/pass
- Does two lines far away from each other touch? (no) 	 1.3335 microseconds/pass
- Does two lines far away from each other touch? (no) 	 1.1360 microseconds/pass
- Does two polygons nestled on each other touch? (yes) 	 18.9363 microseconds/pass
- Does two polygons nestled on each other enclose? (no) 	 19.8605 microseconds/pass
- Does a big polygon enclose a small one? (yes) 	 163.2592 microseconds/pass
- Does a big complex circle enclose a small complex circle? (yes) 	 1476.7210 microseconds/pass
- Does a big simple diamond enclose a small complex circle? (yes) 	 773.1403 microseconds/pass
- Does a big complex circle enclose a small simple square? (yes) 	 301.4145 microseconds/pass

### Credit
Used a public domain function by Darel Rex Finley (http://alienryderflex.com/intersect/) as a base for line intersection.

