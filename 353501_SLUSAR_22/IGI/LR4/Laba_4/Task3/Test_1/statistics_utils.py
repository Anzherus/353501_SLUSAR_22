"""
Модуль статистических расчетов
"""
import math
from typing import List


class SeriesStatistics:
    def __init__(self, sequence: List[float]):
        self.sequence = sequence

    def mean(self) -> float:
        """Вычислить среднее арифметическое последовательности"""
        return sum(self.sequence) / len(self.sequence) if self.sequence else 0.0

    def median(self) -> float:
        """Вычислить медиану последовательности"""
        sorted_seq = sorted(self.sequence)
        n = len(sorted_seq)
        if n == 0:
            return 0.0
        if n % 2 == 1:
            return sorted_seq[n // 2]
        return (sorted_seq[n // 2 - 1] + sorted_seq[n // 2]) / 2

    def mode(self) -> List[float]:
        """Рассчитать моду(ы) последовательности"""
        if not self.sequence:
            return []

        freq = {}
        for num in self.sequence:
            freq[num] = freq.get(num, 0) + 1

        max_freq = max(freq.values())
        return [num for num, count in freq.items() if count == max_freq]

    def variance(self) -> float:
        """Вычислить дисперсию последовательности"""
        if not self.sequence:
            return 0.0
        mean_val = self.mean()
        return sum((x - mean_val) ** 2 for x in self.sequence) / len(self.sequence)

    def std_deviation(self) -> float:
        """Рассчитать стандартное отклонение последовательности"""
        return math.sqrt(self.variance())

    def get_statistics(self) -> dict:
        """Вернуть всю статистику в виде словаря"""
        return {
            'mean': self.mean(),
            'median': self.median(),
            'mode': self.mode(),
            'variance': self.variance(),
            'std_deviation': self.std_deviation(),
            'sequence_length': len(self.sequence)
        }