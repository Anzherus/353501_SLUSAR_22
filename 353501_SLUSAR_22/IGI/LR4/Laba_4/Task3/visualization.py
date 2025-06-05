"""
Module for visualization
"""

import matplotlib.pyplot as plt

def plot_results(results: List[Dict], filename: str = 'arcsin_plot.png'):
    """
    Plot comparison of series and math arcsin results.
    """
    if len(results) < 2:
        print("Need at least 2 points to plot")
        return
    
    x = [r['x'] for r in results]
    y_series = [r['result'] for r in results]
    y_math = [r['math_result'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y_series, 'bo-', label='Series Expansion')
    plt.plot(x, y_math, 'r--', label='Math.asin')
    
    plt.title('Arcsin Calculation Comparison')
    plt.xlabel('x value')
    plt.ylabel('arcsin(x)')
    plt.grid(True)
    plt.legend()
    
    plt.savefig(filename)
    plt.close()
    print(f"Plot saved as {filename}")