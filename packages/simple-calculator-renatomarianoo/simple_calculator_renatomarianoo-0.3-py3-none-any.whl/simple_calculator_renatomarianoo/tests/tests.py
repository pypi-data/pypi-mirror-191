from simple_calculator_renatomarianoo.calculator import Calculator
import unittest


def make_order():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare


ordered, compare = make_order()
unittest.defaultTestLoader.sortTestMethodsUsing = compare


class CalculatorTests(unittest.TestCase):
    """ Tests for Calculator Program. Includes tests for each operation and to validate the user input value"""
    @ordered
    def test_add(self):
        result = Calculator(2).add()
        self.assertEqual(result, 2)

    @ordered
    def test_subtract(self):
        result = Calculator(4).subtract()
        self.assertEqual(result, -2)

    @ordered
    def test_multiply(self):
        result = Calculator(-2).multiply()
        self.assertEqual(result, 4)

    @ordered
    def test_divide(self):
        result = Calculator(2).divide()
        self.assertEqual(result, 2)

    @ordered
    def test_expon(self):
        result = Calculator(4).expon()
        self.assertEqual(result, 16)

    @ordered
    def test_n_root(self):
        result = Calculator(2).n_root()
        self.assertEqual(result, 4)

    @ordered
    def test_divide_by_zero(self):
        """Checks if the division by zero returns the value in memory, here more precisely first argument = 5.0"""
        result = Calculator(0).divide()
        self.assertEqual(result, 4)

    @ordered
    def test_add_invalid_input(self):
        """ Input values are passed from functions to validation function
            Memory_value is passed directly from the main.
        """
        self.assertRaises(ValueError, Calculator('five').add())


if __name__ == '__main__':
    unittest.main()
