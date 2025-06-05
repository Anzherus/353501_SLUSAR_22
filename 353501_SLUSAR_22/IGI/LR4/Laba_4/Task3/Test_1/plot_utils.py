"""
Модуль для построения графиков результатов
"""
from typing import List

class SeriesPlotter:
    @staticmethod
    def plot_series(x_values: List[float], series_values: List[float],
                   math_values: List[float], eps: float) -> None:
        """PПостройте графики результатов ряда и математической функции"""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_values, series_values, 'b-', label='Series Approximation')
        ax.plot(x_values, math_values, 'r--', label='math.asin()')

        ax.set_xlabel('x values')
        ax.set_ylabel('arcsin(x)')
        ax.set_title(f'arcsin Function Comparison (eps={eps})')
        ax.grid(True)
        ax.legend()

        # Добавить аннотацию для точки с максимальной разницей
        max_diff_idx = max(range(len(x_values)),
                          key=lambda i: abs(series_values[i] - math_values[i]))
        max_diff_x = x_values[max_diff_idx]
        max_diff = abs(series_values[max_diff_idx] - math_values[max_diff_idx])

        ax.annotate(
            f'Max difference: {max_diff:.4f}\nat x={max_diff_x:.2f}',
            xy=(max_diff_x, series_values[max_diff_idx]),
            xytext=(10, 10), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->'))

        plt.show()

    @staticmethod
    def save_plot(filename: str = 'arcsin_comparison.png') -> None:
        """Сохранить график в файл"""
        import matplotlib.pyplot as plt
        plt.savefig(filename)
        print(f"Plot saved as {filename}")