"""
Module for arcsin calculation using power series expansion
"""

import math
from typing import Tuple

def calculate_arcsin_series(x: float, eps: float, max_iter: int = 500) -> Tuple[float, int]:
    """
    Compute arcsin(x) using power series expansion.
    """
    if abs(x) >= 1:
        raise ValueError("|x| must be < 1 for series convergence")
    
    result = 0.0
    term = x
    n = 0
    
    while abs(term) > eps and n < max_iter:
        result += term
        n += 1
        term = term * (x ** 2) * (2 * n - 1) ** 2 / (2 * n * (2 * n + 1))
    
    if n == max_iter:
        print(f"Warning: Reached maximum iterations ({max_iter})")
    
    return result, n

def math_arcsin(x: float) -> float:
    """
    Compute arcsin(x) using math module for comparison.
    """
    return math.asin(x)