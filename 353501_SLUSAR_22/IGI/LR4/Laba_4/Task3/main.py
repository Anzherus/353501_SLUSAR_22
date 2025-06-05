"""
Arcsin(x) Calculator using Power Series Expansion
Lab Work #1: Numerical Methods for Special Functions
Version: 3.0
Developer: Slusar Stanislav 
Date: 2025-15-04
"""

from arcsin_series import calculate_arcsin_series, math_arcsin
from initialization import initialize_from_input, initialize_from_generator
from input_utils import input_eps
from statistics import calculate_stats
from visualization import plot_results
from typing import List, Dict

def print_results_table(x: float, n: int, fx: float, math_fx: float, eps: float) -> None:
    """
    Print results in table format.
    """
    print("\n+-------+-------+-----------+-----------+-------+")
    print("|   x   |   n   |   F(x)    | Math F(x) |  eps  |")
    print("+-------+-------+-----------+-----------+-------+")
    print(f"| {x:.3f} | {n:^5} | {fx:.7f} | {math_fx:.7f} | {eps:.1e} |")
    print("+-------+-------+-----------+-----------+-------+")

def print_stats(stats: Dict[str, float]) -> None:
    """
    Print calculated statistics.
    """
    print("\nStatistics:")
    print(f"Mean: {stats['mean']:.6f}")
    print(f"Median: {stats['median']:.6f}")
    print(f"Mode: {stats['mode']:.6f}")
    print(f"Variance: {stats['variance']:.6f}")
    print(f"Standard deviation: {stats['stdev']:.6f}")
    print(f"Average iterations: {stats['avg_iterations']:.1f}")

def main() -> None:
    """Main program loop."""
    results: List[Dict] = []
    
    print("\n=== Arcsin(x) Calculator ===")
    print("Computes arcsin(x) using power series expansion")
    
    while True:
        try:
            print("\nChoose input method:")
            print("1 - Manual input")
            print("2 - Random generation")
            choice = input("Your choice (1/2): ").strip()
            
            if choice == '1':
                x = initialize_from_input()
            elif choice == '2':
                x = initialize_from_generator()
                print(f"\nGenerated x = {x:.3f}")
            else:
                print("Error: invalid choice")
                continue
                
            eps = input_eps()
            
            # Calculate results
            fx, n = calculate_arcsin_series(x, eps)
            math_fx = math_arcsin(x)
            
            # Store results
            results.append({
                'x': x,
                'result': fx,
                'math_result': math_fx,
                'iterations': n,
                'eps': eps
            })
            
            # Print current results
            print_results_table(x, n, fx, math_fx, eps)
            
            # Calculate and print statistics if we have enough data
            if len(results) >= 2:
                stats = calculate_stats(results)
                print_stats(stats)
                plot_results(results)
            
            if input("\nRepeat? (y/n): ").strip().lower() != 'y':
                # Final results and plot
                if len(results) >= 1:
                    if len(results) >= 2:
                        stats = calculate_stats(results)
                        print("\nFinal statistics:")
                        print_stats(stats)
                    plot_results(results, 'final_arcsin_plot.png')
                print("\nProgram completed.")
                break
                
        except ValueError as e:
            print(f"\nError: {e}")
        except KeyboardInterrupt:
            print("\nProgram interrupted")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            break

if __name__ == "__main__":
    main()