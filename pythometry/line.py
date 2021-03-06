import math


class Line(object):

    REPRTEMPLATE = "pythometry.Line ({} {}) - ({} {}) d:{} l:{}"
    DECIMALPOINTSACCURACY = 8

    def __init__(self, origo_x, origo_y, endpoint_x=None, endpoint_y=None, radii=None, length=None):
        self.origo_x = origo_x
        self.origo_y = origo_y
        self.endpoint_x = endpoint_x
        self.endpoint_y = endpoint_y
        self.radii = radii
        self.length = length
        self.boundingbox = ((None, None), (None, None))
        self.points = ((None, None), (None, None))
        if endpoint_x is not None and endpoint_y is not None:
            self.updateendpoints(endpoint_x, endpoint_y)
        elif radii is not None and length is not None:
            self.updatevector(radii, length)
        else:
            raise AttributeError("Need endpoints or radii and length.")

    def updateendpoints(self, endpoint_x, endpoint_y):
        self.endpoint_x = endpoint_x
        self.endpoint_y = endpoint_y
        self._updatedeltas()
        self._updateradii()
        self._updatelength()
        self._updatepoints()
        self._updateboundingbox()

    def updatevector(self, radii=None, length=None):
        if radii is None:
            radii = self.radii
        if length is None:
            length = self.length
        self.endpoint_x = float(math.cos(radii) * length)
        self.endpoint_y = float(math.sin(radii) * length)
        self._updatedeltas()
        self._updatepoints()
        self._updateboundingbox()

    def _updateboundingbox(self):
        minx, maxx = sorted([self.origo_x, self.endpoint_x])
        miny, maxy = sorted([self.origo_y, self.endpoint_y])
        self.boundingbox = ((minx, miny), (maxx, maxy))

    def _updatedeltas(self):
        self.deltax = self.endpoint_x - self.origo_x
        self.deltay = self.endpoint_y - self.origo_y

    def _updateradii(self):
        try:
            self.radii = self._getradii(self.deltax, self.deltay)
        except TypeError:
            print(type(self.deltax), type(self.deltay))
            raise

    def _updatepoints(self):
        self.points = ((self.origo_x, self.origo_y), (self.endpoint_x, self.endpoint_y))

    @staticmethod
    def _getradii(deltax, deltay):
        return math.atan2(deltay, deltax)

    def _updatelength(self):
        self.length = math.sqrt(self.deltax ** 2 + self.deltay ** 2)

    def __repr__(self):
        return self.REPRTEMPLATE.format(self.origo_x, self.origo_y,
                                        self.endpoint_x, self.endpoint_y,
                                        math.degrees(self.radii), self.length)

    @staticmethod
    def fit_radii(radii_to_fit, radii_for_reference=0):
        radii_to_fit -= radii_for_reference
        radii_to_fit += math.pi
        radii_to_fit %= math.pi * 2
        radii_to_fit -= math.pi * 2
        radii_to_fit %= -math.pi * 2
        radii_to_fit += math.pi
        radii_to_fit += radii_for_reference
        return radii_to_fit

    def get_radii_range_from_vector(self, origo_x, origo_y, radii):
        line1 = Line(origo_x, origo_y, self.origo_x, self.origo_y)
        line2 = Line(origo_x, origo_y, self.endpoint_x, self.endpoint_y)
        radii1 = self.fit_radii(line1.radii, radii)
        radii2 = self.fit_radii(line2.radii, radii)
        smallest_radii, biggest_radii = sorted([radii1, radii2])
        return smallest_radii, biggest_radii

    def crosses_vector(self, origo_x, origo_y, radii):
        smallest_radii, biggest_radii = self.get_radii_range_from_vector(origo_x, origo_y, radii)
        return smallest_radii <= radii <= biggest_radii

    def _boundingbox_intersects(self, other):
        self_minpoint, self_maxpoint = self.boundingbox
        other_minpoint, other_maxpoint = other.boundingbox
        return self_minpoint[0] <= other_maxpoint[0] and self_minpoint[1] <= other_maxpoint[1] and \
            self_maxpoint[0] >= other_minpoint[0] and self_maxpoint[1] >= other_minpoint[1]

    def _shares_points(self, other):
        for point in other.points:
            if point in self.points:
                return point
        return None

    def _touchespoints(self, other):
        for point in other.points:
            if self._touchespoint(point):
                return point
        return None

    def _touchespoint(self, point):
        px, py = point
        if not self.boundingbox[0][0] < px < self.boundingbox[1][0] and \
           not self.boundingbox[0][1] < py < self.boundingbox[1][1]:
            return False
        px -= self.origo_x
        py -= self.origo_y
        if self.deltax == 0:
            return px in self.points
        k = round(float(self.deltay) / float(self.deltax), self.DECIMALPOINTSACCURACY)
        return k == round(float(py) / float(px), self.DECIMALPOINTSACCURACY)

    def touches(self, other):
        return self.findtouchpoint(other) is not None

    def converges_on(self, other):
        otherradii = other.radii
        linebetween = Line(self.origo_x, self.origo_y, other.origo_x, other.origo_y)
        otherradii -= self.radii
        otherradii = self.fit_radii(otherradii)
        linebetween.updatevector(linebetween.radii - self.radii)
        return (linebetween.endpoint_y > self.origo_y and otherradii < 0) or \
               (linebetween.endpoint_y < self.origo_y and otherradii > 0)

    def findtouchpoint(self, other):
        if self.length == 0 or other.length == 0:
            return None

        if not self._boundingbox_intersects(other):
            return None

        point = self._shares_points(other)
        if point is not None:
            return point

        point = self._touchespoints(other)
        if point is not None:
            return point

        if self.parallel_to(other):
            return None
        
        #  (1) Translate the system so that point A is on the origin.

        distance_to_intersection_along_own_axis = self.distance_to_collision_with(other)
        if distance_to_intersection_along_own_axis is None:
            return None

        if not 0 <= distance_to_intersection_along_own_axis <= self.length:
            return None

        thecos = (self.endpoint_x - self.origo_x) / float(self.length)
        thesin = (self.endpoint_y - self.origo_y) / float(self.length)

        x = self.origo_x + distance_to_intersection_along_own_axis * thecos
        y = self.origo_y + distance_to_intersection_along_own_axis * thesin
        x = round(x, self.DECIMALPOINTSACCURACY)
        y = round(y, self.DECIMALPOINTSACCURACY)
        return (x, y)

    def distance_to_collision_with(self, other):
        self_endpoint_x = self.endpoint_x - self.origo_x
        self_endpoint_y = self.endpoint_y - self.origo_y
        other_origo_x = other.origo_x - self.origo_x
        other_origo_y = other.origo_y - self.origo_y
        other_endpoint_x = other.endpoint_x - self.origo_x
        other_endpoint_y = other.endpoint_y - self.origo_y

        thecos = self_endpoint_x / float(self.length)
        thesin = self_endpoint_y / float(self.length)

        tempx = other_origo_x * thecos + other_origo_y * thesin
        other_origo_y = other_origo_y * thecos - other_origo_x * thesin
        other_origo_x = tempx
        tempx = other_endpoint_x * thecos + other_endpoint_y * thesin
        other_endpoint_y = other_endpoint_y * thecos - other_endpoint_x * thesin
        other_endpoint_x = tempx

        if (other_origo_y < 0.) == (other_endpoint_y < 0.):
            return None

        return other_endpoint_x + (other_origo_x - other_endpoint_x) * \
               other_endpoint_y / (other_endpoint_y - other_origo_y)

    def parallel_to(self, other):
        return self.radii % (math.pi * 2) == other.radii % (math.pi * 2) or \
           self.radii % (math.pi * 2) == (other.radii + math.pi) % (math.pi * 2)
