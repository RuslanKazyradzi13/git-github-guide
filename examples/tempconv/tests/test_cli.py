import io
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

from tempconv.__main__ import main


def run(*args: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(args))
    return code, out.getvalue().strip(), err.getvalue().strip()


class CliTests(unittest.TestCase):
    def test_prints_result(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            code, out, _ = run("100", "C", "F")
        self.assertEqual(code, 0)
        self.assertEqual(out, "100 °C = 212.00 °F")

    def test_negative_value(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            code, out, _ = run("-40", "C", "F")
        self.assertEqual(code, 0)
        self.assertEqual(out, "-40 °C = -40.00 °F")

    def test_precision_from_environment(self):
        with mock.patch.dict(os.environ, {"TEMPCONV_PRECISION": "3"}):
            _, out, _ = run("1", "C", "F")
        self.assertEqual(out, "1 °C = 33.800 °F")

    def test_invalid_precision_falls_back_to_default(self):
        with mock.patch.dict(os.environ, {"TEMPCONV_PRECISION": "много"}):
            _, out, _ = run("0", "C", "F")
        self.assertEqual(out, "0 °C = 32.00 °F")

    def test_kelvin_has_no_degree_sign(self):
        with mock.patch.dict(os.environ, {"TEMPCONV_PRECISION": "2"}):
            _, out, _ = run("0", "C", "K")
        self.assertEqual(out, "0 °C = 273.15 K")

    def test_unknown_scale_returns_error_code(self):
        code, out, err = run("1", "X", "C")
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("неизвестная шкала", err)


if __name__ == "__main__":
    unittest.main()
