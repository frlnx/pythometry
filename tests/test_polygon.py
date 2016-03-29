from pythometry import Polygon

class TestPolygon(object):

    def setup(self):
        self.bigdiamond = Polygon([(-200, 0), (0, -200), (200, 0), (0, 200)], close=True)
        self.diamond = Polygon([(-50, 0), (0, -50), (50, 0), (0, 50)])
        self.square = Polygon([(-25, -25), (25, -25), (25, 25), (-25, 25)])
        self.tinysquare = Polygon([(-5, -5), (5, -5), (5, 5), (-5, 5)], close=True)
        self.big_u_shape = Polygon([(-100, -100), (-100, 100), (100, 100), (100, -100), (90, -100), (90, 90), (-90, 90), (-90, -100)],
                                   close=True)

    def test_diamond_and_square_overlaps(self):
        assert self.square.touches(self.diamond)

    def test_closed_vs_open(self):
        coords = [(0, 0), (10, 10), (0, 10)]
        openpoly = Polygon(coords)
        closedpoly = Polygon(coords, close=True)
        assert len(openpoly.lines) == 2
        assert len(closedpoly.lines) == 3

    def test_openshape_encloses_tinyclosedshape(self):
        assert self.diamond.encloses(self.tinysquare)

    def test_touching_shapes_does_not_enclose_each_other(self):
        assert not self.diamond.encloses(self.square)
        assert not self.square.encloses(self.diamond)

    def test_bigclosedshape_encloses_openshape(self):
        assert self.bigdiamond.encloses(self.square)

    def test_big_u_shape_encloses_openshape(self):
        assert not self.big_u_shape.encloses(self.tinysquare)