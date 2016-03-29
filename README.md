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
- Does two crossed lines touch? (yes) 	 10.4826 microseconds/pass
- Where does two crossed lines touch? 	 10.3653 microseconds/pass
- Does two parallel lines on top of each other touch? (yes) 	 6.5225 microseconds/pass
- Where does two parallel lines on top of each other touch? 	 6.3153 microseconds/pass
- Does two non overlapping parallel lines touch? (no, but close) 	 8.2568 microseconds/pass
- Where does two non overlapping parallel lines touch? 	 8.1087 microseconds/pass
- Does two lines far away from each other touch? (no) 	 1.2200 microseconds/pass
- Does two lines far away from each other touch? (no) 	 1.0632 microseconds/pass
- Does two polygons nestled on each other touch? (yes) 	 19.7406 microseconds/pass
- Does two polygons nestled on each other enclose? (no) 	 19.9524 microseconds/pass
- Does a big polygon enclose a small one? (yes) 	 164.8557 microseconds/pass
- Does a big complex circle enclose a small complex circle? (yes) 	 131.8628 microseconds/pass
- Does a big simple diamond enclose a small complex circle? (yes) 	 782.9450 microseconds/pass
- Does a big complex circle enclose a small simple square? (yes) 	 140.6211 microseconds/pass

### Credit
Used a public domain function by Darel Rex Finley (http://alienryderflex.com/intersect/) as a base for line intersection.

