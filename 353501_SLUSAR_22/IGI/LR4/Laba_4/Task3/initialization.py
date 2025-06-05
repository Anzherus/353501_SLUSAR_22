"""
Module for data initialization methods
"""

import random
from input_utils import input_float

def initialize_from_input() -> float:
    """
    Initialize x value from user input.
    """
    return input_float("Enter x value (|x| < 1): ", -1.0, 1.0)

def initialize_from_generator() -> float:
    """
    Initialize x value using random generator.
    """
    return random.uniform(-0.99, 0.99)