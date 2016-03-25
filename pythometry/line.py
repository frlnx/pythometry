import math


class Line(object):

    REPRTEMPLATE = "pythometry.Line ({} {}) - ({} {}) r:{} l:{}"

    def __init__(self, origo_x, origo_y, endpoint_x=None, endpoint_y=None, radii=None, length=None):
        self.origo_x = origo_x
        self.origo_y = origo_y
        self.endpoint_x = endpoint_x
        self.endpoint_y = endpoint_y
        self.radii = radii
        self.length = length
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

    def updatevector(self, radii, length):
        self.endpoint_x = float(math.cos(radii) * length)
        self.endpoint_y = float(math.sin(radii) * length)
        self._updatedeltas()
        self._updatepoints()

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
                                        self.radii, self.length)

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

    def touches(self, other):
        for point in self.points:
            if point in other.points:
                return True
        inverseradii = self.fit_radii(other.radii - math.pi)
        return self.crosses_vector(other.origo_x, other.origo_y, other.radii) and \
            self.crosses_vector(other.endpoint_x, other.endpoint_y, inverseradii)

    def touchpoint(self, other):
        for point in self.points:
            if point in other.points:
                return point
        return (float('nan'), float('nan'))