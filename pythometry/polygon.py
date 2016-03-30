from pythometry.line import Line


class LineCollection(object):

    def __init__(self, lines):
        self.lines = list(lines)
        self.points = [line.points[0] for line in self.lines]
        self.points += [line.points[1] for line in self.lines]
        self.boundingbox = ((None, None), (None, None))
        self._updateboundingbox()

    def append(self, line):
        self.lines.append(line)
        self.points += line.points
        self._updateboundingbox()

    def __iadd__(self, other):
        self.lines += other
        self.points += [line.points[0] for line in other.lines]
        self.points += [line.points[1] for line in other.lines]
        self._updateboundingbox()

    def __iter__(self):
        return self.lines.__iter__()

    def _updateboundingbox(self):
        if self.points == []:
            return
        xcoords = [point[0] for point in self.points]
        ycoords = [point[1] for point in self.points]
        minx = min(xcoords)
        maxx = max(xcoords)
        miny = min(ycoords)
        maxy = max(ycoords)
        self.boundingbox = ((minx, miny), (maxx, maxy))

    def _boundingbox_intersects(self, other):
        self_minpoint, self_maxpoint = self.boundingbox
        other_minpoint, other_maxpoint = other.boundingbox
        return self_minpoint[0] <= other_maxpoint[0] and self_minpoint[1] <= other_maxpoint[1] and \
            self_maxpoint[0] >= other_minpoint[0] and self_maxpoint[1] >= other_minpoint[1]

    def touches(self, other):
        if len(self.lines) < len(other.lines):
            return other.touches(self)
        if not self._boundingbox_intersects(other):
            return False
        for line in self.lines:
            if not line._boundingbox_intersects(other):
                continue
            for line2 in other.lines:
                if line.touches(line2):
                    return True
        return False

class Polygon(LineCollection):

    def __init__(self, points, close=False):
        self.points = points
        if close:
            self.points.append(self.points[0])
        self.closed = self.points[0] == self.points[-1]
        self.lines = []
        self._generatelines()
        self.boundingbox = ((None, None), (None, None))
        self._updateboundingbox()

    def _generatelines(self):
        lastpoint = self.points[0]
        self.lines = []
        for point in self.points[1:]:
            x, y = lastpoint
            x2, y2 = point
            self.lines.append(Line(x, y, x2, y2))
            lastpoint = point

    def encloses(self, other):
        if self.touches(other):
            return False
        lines = self.lines
        if not self.closed:
            lines = list(lines)
            endpoint_x, endpoint_y = lines[-1].points[-1]
            origo_x, origo_y = lines[0].points[0]
            closingline = Line(origo_x, origo_y, endpoint_x, endpoint_y)
            lines.append(closingline)
        anypoint_x, anypoint_y = other.lines[0].points[0]
        outsidepoint_x, outsidepoint_y = [coord - 1 for coord in self.boundingbox[0]]
        breakoutline = Line(anypoint_x, anypoint_y, outsidepoint_x, outsidepoint_y)
        touchpoints = []
        for line in self.lines:
            touchpoint = line.findtouchpoint(breakoutline)
            if touchpoint is not None:
                touchpoints.append(touchpoint)
        return len(set(touchpoints)) % 2 == 1
