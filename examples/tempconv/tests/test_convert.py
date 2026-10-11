import unittest

from tempconv import convert, normalize_scale


class ConvertTests(unittest.TestCase):
    def test_freezing_point_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(convert(0, "C", "F"), 32)

    def test_boiling_point_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(convert(100, "C", "F"), 212)

    def test_minus_forty_is_same_in_both_scales(self):
        self.assertAlmostEqual(convert(-40, "F", "C"), -40)

    def test_absolute_zero_in_kelvin(self):
        self.assertAlmostEqual(convert(0, "K", "C"), -273.15)

    def test_same_scale_returns_same_value(self):
        self.assertAlmostEqual(convert(36.6, "C", "C"), 36.6)

    def test_round_trip(self):
        value = 451
        self.assertAlmostEqual(convert(convert(value, "F", "K"), "K", "F"), value)

    def test_scale_is_case_insensitive(self):
        self.assertAlmostEqual(convert(10, "c", "k"), 283.15)

    def test_unknown_scale_raises_error(self):
        with self.assertRaises(ValueError):
            convert(1, "X", "C")

    def test_below_absolute_zero_raises_error(self):
        with self.assertRaises(ValueError):
            convert(-300, "C", "K")


class NormalizeScaleTests(unittest.TestCase):
    def test_strips_spaces_and_uppercases(self):
        self.assertEqual(normalize_scale(" f "), "F")


if __name__ == "__main__":
    unittest.main()
