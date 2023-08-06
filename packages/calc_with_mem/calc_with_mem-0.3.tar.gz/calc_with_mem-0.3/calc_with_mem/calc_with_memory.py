# Function from math module is imported to avoid division by zero related issues working with float numbers
from math import isclose


def _pass_int_or_float(argument):
    """
    Argument validation function.
    The argument is passed only if it is float or integer.
    Otherwise, assertion error message is provided
    """
    assert isinstance(argument, (int, float)), f'Expected integer or float value, received {argument}'
    return argument


class Calculator:
    """
    Calculator object can perform these actions:
        Addition (plus method is used) / Subtraction (minus method)
        Multiplication (multiply method) / Division (divide method)
        Take (n) root of a number (root method)
        Reset memory (reset method).
    Calculator has its own attribute memory, meaning it manipulates its starting number 0.0 until the memory is reset.

    Thus, all methods above require just one argument, except reset for which the argument is optional.
        For example,
        calculator.plus(2) adds 2 to the memory, calculator.minus(5) subtracts 5 from the memory,
        calculator.multiply(10) multiplies the memory by 10, calculate.divide(3) divides the memory by 3
        and calculator.root(4) takes 4th root of the memory.
    Reset method calculator.reset(0) by default sets the memory to 0.0,
        but it is allowed to set the memory to the desired value,
        providing an optional argument as calculator.reset(desired_value)

    Calculator works with integer and float numbers, a validation is performed before the methods are used.
    Calculator also prevents division by zero and applies a root operation on a negative number.
    """
    def __init__(self):
        # Own calculator memory is set to 0.0 during the initialization.
        self.memory = 0.0

    def plus(self, argument: float):
        # Validates and adds an argument to the memory
        self.memory += _pass_int_or_float(argument)

    def minus(self, argument: float):
        # Validates and subtracts an argument from the memory
        self.memory -= _pass_int_or_float(argument)

    def multiply(self, argument: float):
        # Validates the argument and multiplies the memory by it
        self.memory = self.memory * _pass_int_or_float(argument)

    def divide(self, argument: float):
        # Validates the argument before the memory is divided by it
        if isclose(0, _pass_int_or_float(argument)):
            raise ValueError(f'Division by zero or close to it value {argument} is not allowed by the calculator')
        else:
            self.memory = self.memory / argument

    def root(self, argument: float):
        # Validates the argument and prevents applying root operation on a negative memory value
        if self.memory < 0:
            raise ValueError(f'Root from negative number {self.memory} is not allowed by the calculator')
        else:
            self.memory = self.memory ** (1 / _pass_int_or_float(argument))

    def reset(self, set_memory=0.0):
        # Resets the memory 0.0 by default or to a provided and validated value
        self.memory = _pass_int_or_float(set_memory)
