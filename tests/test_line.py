import math
from pythometry.line import Line
import pytest

class TestLine(object):

    def setup(self):
        self.horisontal_at_ten = Line(0, 10, endpoint_x=100, endpoint_y=10)
        self.horisontal_at_twenty = Line(0, 20, endpoint_x=100, endpoint_y=20)
        self.vertical_at_ten = Line(10, 0, endpoint_x=10, endpoint_y=100)
        self.vertical_at_twenty = Line(20, 0, endpoint_x=20, endpoint_y=100)
        self.diagonal_topleft_bottomright = Line(0, 0, endpoint_x=100, endpoint_y=100)
        self.diagonal_bottomleft_topright = Line(0, 100, endpoint_x=100, endpoint_y=0)
        self.center_to_right = Line(50, 50, radii=0, length=50)
        self.center_to_topleft = Line(50, 50, radii=((math.pi / 4.0) * 5), length=50)
        self.bottomleft_to_center = Line(0, 100, endpoint_x=50, endpoint_y=50)
        self.topright_to_center = Line(100, 100, endpoint_x=50, endpoint_y=50)
        self.eighth = (math.pi / 4.0)
        self.overlapping_left = Line(0, 0, 10, 0)
        self.overlapping_right = Line(5, 0, 15, 0)
        self.low_cross_line_one = Line(0, 30, 100, 70)
        self.low_cross_line_two = Line(0, 70, 100, 30)
        self.low_asymetrical_cross_line_one = Line(10, 30, 110, 70)
        self.low_asymetrical_cross_line_two = Line(-10, 70, 90, 30)
        self.shifted_diagonal_cross_line_one = Line(10, 30, 90, 70)
        self.shifted_diagonal_cross_line_two = Line(30, 90, 70, 10)
        self.right_shifted_diagonal_one = Line(10, 30, 90, 70)
        self.right_shifted_diagonal_two = Line(10, 70, 90, 30)
        self.line1 = Line(0, 0, 100, 100)
        self.line2 = Line(100, 0, 0, 100)

    def test_overlapping_on_same_plane(self):
        assert self.overlapping_left.touches(self.overlapping_right)

    def test_overlapping_on_same_plane_touchpoint(self):
        assert self.overlapping_left._boundingbox_intersects(self.overlapping_right)
        assert self.overlapping_left.findtouchpoint(self.overlapping_right) == (5, 0)

    def test_center_to_right_does_not_touch_vertical_at_ten(self):
        assert not self.center_to_right.touches(self.vertical_at_ten)

    def test_bottomleft_to_center_does_not_touch_horisontal_at_ten(self):
        assert not self.bottomleft_to_center.touches(self.horisontal_at_ten)

    def test_radii(self):
        assert self.horisontal_at_ten.radii == 0
        assert self.vertical_at_ten.radii == (math.pi / 2.0)
        assert self.diagonal_topleft_bottomright.radii == (math.pi / 4.0)

    def test_length(self):
        assert self.horisontal_at_ten.length == 100
        assert self.vertical_at_ten.length == 100

    def test_horisontal_dont_touch(self):
        assert not self.horisontal_at_ten.touches(self.horisontal_at_twenty)

    def test_vertical_dont_touch(self):
        assert not self.vertical_at_ten.touches(self.vertical_at_twenty)

    def test_horisontal_touches_diagonal(self):
        assert self.horisontal_at_ten._boundingbox_intersects(self.diagonal_bottomleft_topright)
        assert self.horisontal_at_ten.touches(self.diagonal_bottomleft_topright)

        assert self.horisontal_at_ten._boundingbox_intersects(self.diagonal_topleft_bottomright)
        assert self.horisontal_at_ten.touches(self.diagonal_topleft_bottomright)

        assert self.horisontal_at_twenty._boundingbox_intersects(self.diagonal_bottomleft_topright)
        assert self.horisontal_at_twenty.touches(self.diagonal_bottomleft_topright)

        assert self.horisontal_at_twenty._boundingbox_intersects(self.diagonal_topleft_bottomright)
        assert self.horisontal_at_twenty.touches(self.diagonal_topleft_bottomright)

    def test_horisontal_touches_vertical(self):
        assert self.horisontal_at_ten.touches(self.vertical_at_ten)
        assert self.horisontal_at_ten.touches(self.vertical_at_twenty)
        assert self.horisontal_at_twenty.touches(self.vertical_at_ten)
        assert self.horisontal_at_twenty.touches(self.vertical_at_twenty)

    def test_diagonals_touch(self):
        assert self.diagonal_topleft_bottomright.touches(self.diagonal_bottomleft_topright)

    def test_centers_touch(self):
        assert self.center_to_right.touches(self.center_to_topleft)
        assert self.center_to_right.touches(self.topright_to_center)
        assert self.topright_to_center.touches(self.bottomleft_to_center)

    def test_getradii_right(self):
        right = 0
        assert Line._getradii(4, 0) == right

    def test_getradii_downright(self):
        downright = (math.pi / 4.0)
        assert Line._getradii(4, 4) == downright

    def test_getradii_down(self):
        down = (math.pi / 2.0)
        assert Line._getradii(0, 4) == down

    def test_getradii_downleft(self):
        downleft = self.eighth * 3
        assert Line._getradii(-4, 4) == downleft

    def test_getradii_left(self):
        left = math.pi
        assert Line._getradii(-4, 0) == left

    def test_getradii_upleft(self):
        upleft = -self.eighth * 3
        assert Line._getradii(-4, -4) == upleft

    def test_getradii_up(self):
        up = -math.pi / 2.0
        assert Line._getradii(0, -4) == up

    def test_getradii_upright(self):
        upright = -self.eighth
        assert Line._getradii(4, -4) == upright

    def test_get_radii_range_topleft_downright(self):
        expected = math.pi / 4.0
        smallest_radii, biggest_radii = self.diagonal_bottomleft_topright.get_radii_range_from_vector(0, 0, expected)
        assert smallest_radii < expected
        assert expected < biggest_radii

    def test_get_radii_range_bottom_up(self):
        expected = -math.pi / 2.0
        smallest_radii, biggest_radii = self.diagonal_bottomleft_topright.get_radii_range_from_vector(50, 100, expected)
        assert smallest_radii < expected
        assert expected < biggest_radii

    def test_get_radii_range_far_bottom_up(self):
        expected = -math.pi / 2.0
        smallest_radii, biggest_radii = self.diagonal_bottomleft_topright.get_radii_range_from_vector(50, 150, expected)
        assert smallest_radii < expected
        assert expected < biggest_radii

    def test_get_radii_range_right_upleft(self):
        expected = -3 * math.pi / 4.0
        smallest_radii, biggest_radii = self.diagonal_bottomleft_topright.get_radii_range_from_vector(100, 50, expected)
        assert smallest_radii < expected
        assert expected < biggest_radii

    def test_get_radii_range_right_downleft(self):
        expected = 3 * math.pi / 4.0
        smallest_radii, biggest_radii = self.diagonal_topleft_bottomright.get_radii_range_from_vector(100, 50, expected)
        assert smallest_radii < expected
        assert expected < biggest_radii

    def test_crosses_vector_topleft_downright(self):
        assert self.diagonal_bottomleft_topright.crosses_vector(0, 0, math.pi / 4.0)

    def test_crosses_vector_bottom_up(self):
        assert self.diagonal_bottomleft_topright.crosses_vector(50, 100, -math.pi / 2.0)

    def test_touchpoint_topleft_cross(self):
        assert self.horisontal_at_ten.findtouchpoint(self.vertical_at_ten) == (10, 10)

    def test_touchpoint_diagonals_middle(self):
        actual = self.diagonal_bottomleft_topright.findtouchpoint(self.diagonal_topleft_bottomright)
        actual = (round(actual[0], 3), round(actual[1], 3))
        assert actual == (50.0, 50.0)

    def test_touchpoint_low_cross_middle(self):
        assert self.low_cross_line_one.findtouchpoint(self.low_cross_line_two) == (50, 50)

    def test_touchpoint_low_asymetrical_cross_middle(self):
        actual = self.low_asymetrical_cross_line_one.findtouchpoint(self.low_asymetrical_cross_line_two)
        actual = (round(actual[0], 3), round(actual[1], 3))
        assert actual == (50, 46)

    def test_touchpoint_shifted_diagonal_cross_middle(self):
        actual = self.shifted_diagonal_cross_line_one.findtouchpoint(self.shifted_diagonal_cross_line_two)
        actual = (round(actual[0], 3), round(actual[1], 3))
        assert actual == (50, 50)

    def test_touchpoint_right_shifted_diagonal_cross_middle(self):
        actual = self.right_shifted_diagonal_one.findtouchpoint(self.right_shifted_diagonal_two)
        actual = (round(actual[0], 3), round(actual[1], 3))
        assert actual == (50, 50)

    def test_touchpoint_out_of_range(self):
        assert self.bottomleft_to_center.findtouchpoint(self.vertical_at_ten) is None

    def test_touchpoint_behind(self):
        assert self.center_to_right.findtouchpoint(self.vertical_at_ten) is None

    def test_touchpoint_nonexistant(self):
        assert self.horisontal_at_ten.findtouchpoint(self.horisontal_at_twenty) is None

    def test_boundingbox_intersection(self):
        assert self.diagonal_bottomleft_topright._boundingbox_intersects(self.diagonal_topleft_bottomright)

    def test_boundingbox_nonintersection(self):
        assert not self.bottomleft_to_center._boundingbox_intersects(self.horisontal_at_ten)