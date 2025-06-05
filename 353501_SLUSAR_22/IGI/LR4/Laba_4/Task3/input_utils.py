"""
Module for safe user input handling
"""

def input_float(prompt: str, min_val: float = -1.0, max_val: float = 1.0) -> float:
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
        except KeyboardInterrupt:
            print("\nInput interrupted by user")
            raise

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
        except KeyboardInterrupt:
            print("\nInput interrupted by user")
            raise