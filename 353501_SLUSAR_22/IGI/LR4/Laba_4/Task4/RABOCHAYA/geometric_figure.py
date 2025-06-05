from abc import ABC, abstractmethod
import math


class GeometricFigure(ABC):
    """Абстрактный класс геометрической фигуры"""

    @abstractmethod
    def calculate_area(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass


class FigureColor:
    """Класс цвета фигуры"""

    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        """Свойство цвета"""
        return self._color

    @color.setter
    def color(self, value):
        self._color = value