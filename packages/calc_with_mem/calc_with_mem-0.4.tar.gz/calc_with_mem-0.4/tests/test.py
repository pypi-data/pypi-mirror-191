import unittest

# We will test our Calculator class
from calc_with_mem.calc_with_memory import Calculator

my_calculator = Calculator()    # Calculator class object is created


class TestSum(unittest.TestCase):
    """
    We are testing that the calculator is performing requested operations properly.
    We test all the operations separately and also their combined scenario.
    That makes us to feel much more comfortable.
    """
    def test_add(self):
        # plus method is tested using the chosen memory and the argument
        my_calculator.reset(6.4645)
        my_calculator.plus(10.5445454)
        self.assertEqual(my_calculator.memory, 6.4645+10.5445454)

    def test_subtract(self):
        # minus method is tested using the chosen memory and the argument
        my_calculator.reset(5.55555)
        my_calculator.minus(1.55555)
        self.assertEqual(my_calculator.memory, 5.55555-1.55555)

    def test_multiply(self):
        # multiply method is tested using the chosen memory and the argument
        my_calculator.reset(-1.554545)
        my_calculator.multiply(1.5454545)
        self.assertEqual(my_calculator.memory, -1.554545*1.5454545)

    def test_divide(self):
        # divide  method is tested using the chosen memory and the argument
        my_calculator.reset(100.0)
        my_calculator.divide(3.0)
        self.assertEqual(my_calculator.memory, 100.0/3.0)

    def test_root(self):
        # root method is tested using the chosen memory and the argument
        my_calculator.reset(1000.0)
        my_calculator.root(3.0)
        self.assertEqual(my_calculator.memory, 1000.0**(1/3))

    def mixed(self):
        # A combination of methods is used to increase credibility of the calculator
        my_calculator.reset()
        my_calculator.plus(10.5)
        my_calculator.minus(5)
        my_calculator.multiply(-5.0)
        my_calculator.divide(3.33)
        self.assertEqual(my_calculator.memory, (10.5-5)*(-5.0)/3.33)


if __name__ == '__main__':
    unittest.main()
