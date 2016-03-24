from pythometry import Polygon

class TestPolygon(object):

    def setup(self):
        self.diamond = Polygon([(-100, 0), (0, -100), (100, 0), (0, 100)])
        self.square = Polygon([(-75, -75), (75, -75), (75, 75), (-75, 75)])

    def test_diamond_and_square_overlaps(self):
        assert self.square.touches(self.diamond)