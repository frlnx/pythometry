from pythometry.line import Line


class Polygon(object):

    def __init__(self, points, close=False):
        self.points = points
        if close:
            self.points.append(self.points[0])
        self.lines = []
        self._generatelines()

    def _generatelines(self):
        lastpoint = self.points[0]
        self.lines = []
        for point in self.points[1:]:
            x, y = lastpoint
            x2, y2 = point
            self.lines.append(Line(x, y, x2, y2))

    def touches(self, other):
        for line in self.lines:
            for line2 in other.lines:
                if line.touches(line2):
                    return True
        return False
