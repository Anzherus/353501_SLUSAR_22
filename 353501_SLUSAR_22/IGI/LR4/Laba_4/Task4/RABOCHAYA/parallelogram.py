from geometric_figure import GeometricFigure, FigureColor
import math


class Parallelogram(GeometricFigure):
    """Класс параллелограмма"""
    name = "Параллелограмм"

    def __init__(self, d1, d2, angle, color):
        """
        Конструктор параллелограмма
        :param d1: первая диагональ
        :param d2: вторая диагональ
        :param angle: угол между диагоналями в градусах
        :param color: цвет фигуры
        """
        self.d1 = d1
        self.d2 = d2
        self.angle = angle
        self.color_obj = FigureColor(color)

    @property
    def color(self):
        return self.color_obj.color

    @color.setter
    def color(self, value):
        self.color_obj.color = value

    def calculate_area(self):
        """Вычисление площади параллелограмма по диагоналям и углу между ними"""
        angle_rad = math.radians(self.angle)
        return 0.5 * self.d1 * self.d2 * math.sin(angle_rad)

    def get_parameters(self):
        """Возвращает строку с параметрами фигуры"""
        return ("{name} (диагонали: {d1:.2f} и {d2:.2f}, угол: {angle}°, "
                "цвет: {color}, площадь: {area:.2f})").format(
            name=self.name,
            d1=self.d1,
            d2=self.d2,
            angle=self.angle,
            color=self.color,
            area=self.calculate_area()
        )