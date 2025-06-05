"""
arcsin(x) Calculator using Power Series Expansion
Lab Work #1: Numerical Methods for Special Functions
Version: 3.0
Developer: Slusar Stanislav
Date: 2025-19-04
"""
from typing import List
from arcsin_series import calculate_arcsin_series, math_arcsin
from initialization import initialize_from_input, initialize_from_generator
from statistics_utils import SeriesStatistics
from plot_utils import SeriesPlotter

def print_results(x: float, eps: float) -> None:
    """
  Вычислить и распечатать1 результаты в табличном формате.
    """
    try:
        fx, n, sequence = calculate_arcsin_series(x, eps)
        math_fx = math_arcsin(x)

        stats = SeriesStatistics(sequence).get_statistics()

        print("\n+-------+-------+-----------+-----------+-------+")
        print("|   x   |   n   |   F(x)    | Math F(x) |  eps  |")
        print("+-------+-------+-----------+-----------+-------+")
        print(f"| {x:.3f} | {n:^5} | {fx:.7f} | {math_fx:.7f} | {eps} |")
        print("+-------+-------+-----------+-----------+-------+")

        print("\nSequence Statistics:")
        print(f"Mean: {stats['mean']:.7f}")
        print(f"Median: {stats['median']:.7f}")
        print(f"Mode(s): {', '.join(f'{m:.7f}' for m in stats['mode'])}")
        print(f"Variance: {stats['variance']:.7f}")
        print(f"Standard Deviation: {stats['std_deviation']:.7f}")
        print(f"Sequence length: {stats['sequence_length']}")

    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

def plot_comparison(x_values: List[float], eps: float) -> None:
    """
   Сгенерировать и отобразить сравнительный график для нескольких значений x
   """
    series_values = []
    math_values = []

    for x in x_values:
        fx, _, _ = calculate_arcsin_series(x, eps)
        series_values.append(fx)
        math_values.append(math_arcsin(x))

    plotter = SeriesPlotter()
    plotter.plot_series(x_values, series_values, math_values, eps)
    plotter.save_plot()
    plotter.show_plot()

def main() -> None:
    """Основной цикл программы."""
    print("\n=== arcsin(x) Calculator ===")
    print("Computes arcsin(x) using power series expansion")

    while True:
        try:
            print("\nChoose operation:")
            print("1 - Calculate single value")
            print("2 - Generate comparison plot for multiple values")
            choice = input("Your choice (1/2): ").strip()

            if choice == '1':
                print("\nChoose input method:")
                print("1 - Manual input")
                print("2 - Random generation")
                input_choice = input("Your choice (1/2): ").strip()

                if input_choice == '1':
                    x = initialize_from_input()
                elif input_choice == '2':
                    x = initialize_from_generator()
                    print(f"\nGenerated x = {x:.3f}")
                else:
                    print("Error: invalid choice")
                    continue

                eps = float(input("Enter precision (eps > 0): "))
                if eps <= 0:
                    raise ValueError("Precision must be positive")

                print_results(x, eps)

            elif choice == '2':
                eps = float(input("Enter precision (eps > 0) for plot: "))
                if eps <= 0:
                    raise ValueError("Precision must be positive")

                # Генерация точек для построения графика без numpy
                x_values = [x/100 for x in range(-99, 100, 10)]
                plot_comparison(x_values, eps)

            else:
                print("Error: invalid choice")
                continue

            if input("\nRepeat? (y/n): ").strip().lower() != 'y':
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