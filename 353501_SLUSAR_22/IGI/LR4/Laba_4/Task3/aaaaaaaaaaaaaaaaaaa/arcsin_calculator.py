# arcsin_calculator.py
"""
Arcsin Calculator using Power Series Expansion
Lab Work #3: Numerical Methods for Special Functions with Class Implementation
Version: 3.0
Developer: Slusar Stanislav
Date: 2025-05-02
"""

import math
import random
from typing import List, Tuple
import matplotlib.pyplot as plt
import statistics
from collections import Counter

class ArcsinCalculator:
    """
    Class for calculating arcsin using power series expansion with statistical analysis.
    """
    
    # Class attribute (static)
    version = "3.0"
    
    def __init__(self, x_values: List[float] = None):
        """
        Initialize ArcsinCalculator with optional list of x values.
        """
        self.x_values = x_values if x_values else []
        self.results = []  # Stores tuples of (x, calculated_value, math_value, iterations)
        
    @staticmethod
    def calculate_term(x: float, n: int) -> float:
        """
        Calculate the nth term in the arcsin series.
        """
        if n == 0:
            return x
        return (x ** (2*n + 1)) * math.factorial(2*n) / (4**n * (math.factorial(n)**2) * (2*n + 1))
    
    def calculate_arcsin(self, x: float, eps: float = 1e-6, max_iter: int = 500) -> Tuple[float, int]:
        """
        Compute arcsin(x) using power series expansion.
        
        Args:
            x: Input value (must be |x| < 1)
            eps: Precision threshold
            max_iter: Maximum iterations
            
        Returns:
            Tuple of (result, iterations)
        """
        if abs(x) >= 1:
            raise ValueError("|x| must be < 1 for series convergence")
            
        result = 0.0
        n = 0
        
        while True:
            term = self.calculate_term(x, n)
            result += term
            n += 1
            
            if abs(term) < eps or n >= max_iter:
                break
                
        if n == max_iter:
            print(f"Warning: Reached maximum iterations ({max_iter})")
            
        return result, n
    
    def calculate_math_arcsin(self, x: float) -> float:
        """
        Compute arcsin(x) using math module for comparison.
        """
        return math.asin(x)
    
    def run_calculations(self, eps: float = 1e-6) -> None:
        """
        Run calculations for all x values and store results.
        """
        self.results = []
        for x in self.x_values:
            try:
                calc_value, iterations = self.calculate_arcsin(x, eps)
                math_value = self.calculate_math_arcsin(x)
                self.results.append((x, calc_value, math_value, iterations))
            except ValueError as e:
                print(f"Skipping x = {x}: {e}")
    
    def get_statistics(self) -> dict:
        """
        Calculate and return statistics for the results.
        
        Returns:
            Dictionary with mean, median, mode, variance, std_dev of iterations
        """
        if not self.results:
            return {}
            
        iterations = [r[3] for r in self.results]
        calc_values = [r[1] for r in self.results]
        
        # Calculate mode (most frequent iteration count)
        freq = Counter(iterations)
        mode = max(freq.items(), key=lambda x: x[1])[0]
        
        return {
            'mean': statistics.mean(iterations),
            'median': statistics.median(iterations),
            'mode': mode,
            'variance': statistics.variance(iterations),
            'std_dev': statistics.stdev(iterations),
            'calc_values_mean': statistics.mean(calc_values),
            'calc_values_std': statistics.stdev(calc_values)
        }
    
    def plot_results(self, save_path: str = None) -> None:
        """
        Plot comparison between calculated and math arcsin values.
        
        Args:
            save_path: Optional path to save the plot image
        """
        if not self.results:
            print("No results to plot")
            return
            
        x_values = [r[0] for r in self.results]
        calc_values = [r[1] for r in self.results]
        math_values = [r[2] for r in self.results]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, calc_values, 'b-', label='Series Expansion')
        plt.plot(x_values, math_values, 'r--', label='Math Module')
        
        plt.xlabel('x values')
        plt.ylabel('arcsin(x)')
        plt.title('Comparison of arcsin Calculations')
        plt.legend()
        plt.grid(True)
        
        # Add annotation for the first point
        if len(x_values) > 0:
            plt.annotate(f'First point: x={x_values[0]:.2f}', 
                        xy=(x_values[0], calc_values[0]),
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))
        
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def print_results_table(self) -> None:
        """
        Print results in a formatted table.
        """
        if not self.results:
            print("No results to display")
            return
            
        print("\n+-------+-------+-----------+-----------+-------+")
        print("|   x   |   n   |   F(x)    | Math F(x) |  eps  |")
        print("+-------+-------+-----------+-----------+-------+")
        
        for x, calc, math_val, n in self.results:
            print(f"| {x:.3f} | {n:^5} | {calc:.7f} | {math_val:.7f} | 1e-6 |")
        
        print("+-------+-------+-----------+-----------+-------+")
        
        stats = self.get_statistics()
        if stats:
            print("\nStatistics:")
            print(f"Mean iterations: {stats['mean']:.2f}")
            print(f"Median iterations: {stats['median']}")
            print(f"Mode iterations: {stats['mode']}")
            print(f"Variance: {stats['variance']:.2f}")
            print(f"Standard deviation: {stats['std_dev']:.2f}")


class ArcsinInputHandler:
    """
    Class for handling user input for arcsin calculations.
    """
    
    def __init__(self):
        self.calculator = ArcsinCalculator()
    
    @staticmethod
    def input_float(prompt: str, min_val: float, max_val: float) -> float:
        """
        Safely read a float from user input within [min_val, max_val].
        """
        while True:
            try:
                value = float(input(prompt))
                if not min_val <= value <= max_val:
                    raise ValueError(f"Value must be between {min_val} and {max_val}")
                return value
            except ValueError as e:
                print(f"Error: {e}. Please try again.")
    
    @staticmethod
    def input_eps() -> float:
        """
        Read a positive epsilon value from user.
        """
        while True:
            try:
                eps = float(input("Enter calculation precision (eps > 0): "))
                if eps <= 0:
                    raise ValueError("Precision must be positive")
                return eps
            except ValueError as e:
                print(f"Error: {e}")
    
    def initialize_from_input(self) -> None:
        """
        Initialize x values from user input.
        """
        n = int(self.input_float("How many x values to enter? (1-10): ", 1, 10))
        self.calculator.x_values = []
        for i in range(n):
            x = self.input_float(f"Enter x value {i+1} (|x| < 1): ", -1.0, 1.0)
            self.calculator.x_values.append(x)
    
    def initialize_from_generator(self) -> None:
        """
        Initialize x values using random generator.
        """
        n = int(self.input_float("How many random values to generate? (1-20): ", 1, 20))
        self.calculator.x_values = [random.uniform(-0.99, 0.99) for _ in range(n)]
        print(f"Generated {n} random x values between -0.99 and 0.99")