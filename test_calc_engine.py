import json
import unittest

from calc_engine import CalcError, Calculator, web_eval


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.c = Calculator()

    def test_basic(self):
        self.assertEqual(self.c.calculate("2+3*4"), "14")
        self.assertEqual(self.c.calculate("2^10"), "1024")
        self.assertEqual(self.c.calculate("(1+2)*(3+4)"), "21")

    def test_symbols(self):
        self.assertEqual(self.c.calculate("6×7÷2−1"), "20")
        self.assertEqual(self.c.calculate("√16"), "4")

    def test_trig_degrees_and_radians(self):
        self.assertEqual(self.c.calculate("sin(30)"), "0.5")
        self.assertEqual(self.c.calculate("cos(180)"), "-1")
        self.assertEqual(self.c.calculate("asin(1)"), "90")
        self.c.angle_mode = "rad"
        self.assertEqual(self.c.calculate("cos(pi)"), "-1")

    def test_logs_and_factorials(self):
        self.assertEqual(self.c.calculate("log(1000)"), "3")
        self.assertEqual(self.c.calculate("ln(e)"), "1")
        self.assertEqual(self.c.calculate("5!"), "120")
        self.assertEqual(self.c.calculate("(2+1)!"), "6")
        self.assertEqual(self.c.calculate("nCr(5,2)"), "10")

    def test_implicit_multiplication_and_exp(self):
        self.assertEqual(self.c.calculate("2pi"), "6.28318530718")
        self.assertEqual(self.c.calculate("2(3+4)"), "14")
        self.assertEqual(self.c.calculate("1.5e3"), "1500")

    def test_ans_memory(self):
        self.c.calculate("6*7")
        self.assertEqual(self.c.calculate("ans+8"), "50")

    def test_errors(self):
        for bad in ["1/0", "sqrt(-1)", "ln(0)", "(-8)^(1/3)", "2+", "tan(90)", "70!!", "", "__import__('os')", "open('x')"]:
            with self.subTest(bad=bad):
                with self.assertRaises(CalcError):
                    self.c.calculate(bad)

    def test_web_entry_point(self):
        self.assertEqual(json.loads(web_eval("sin(90)", "deg")), {"ok": True, "text": "1"})
        self.assertFalse(json.loads(web_eval("1/0"))["ok"])


if __name__ == "__main__":
    unittest.main()
