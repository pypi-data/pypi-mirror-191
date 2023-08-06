from simple_calculator_renatomarianoo import Calculator
import unittest

# Constants
NUM1 = 4.0
NUM2 = 2.0


class CalculatorTests(unittest.TestCase):
    """ Tests for Calculator Program. Includes tests for each operation and to validate the user input value"""

    def test_add(self):
        result = Calculator(NUM1, NUM2).add()
        self.assertEqual(result, 6)

    def test_subtract(self):
        result = Calculator(NUM1, NUM2).subtract()
        self.assertEqual(result, 2)

    def test_multiply(self):
        result = Calculator(NUM1, NUM2).multiply()
        self.assertEqual(result, 8)

    def test_divide(self):
        result = Calculator(NUM1, NUM2).divide()
        self.assertEqual(result, 2)

    def test_n_root(self):
        result = Calculator(NUM1, NUM2).n_root()
        self.assertEqual(result, 2)

    def test_expon(self):
        result = Calculator(NUM1, NUM2).expon()
        self.assertEqual(result, 16)

    def test_divide_by_zero(self):
        """Checks if the division by zero returns the value in memory, here more precisely first argument = 5.0"""
        result = Calculator(NUM1, 0).divide()
        self.assertEqual(result, 4)

    def test_add_invalid_input(self):
        """ Input values are passed from functions to validation function
            Memory_value is passed directly from the main.
        """
        self.assertRaises(ValueError, Calculator('five', 'four').add())


if __name__ == '__main__':
    unittest.main()
