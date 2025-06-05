from abc import ABC, abstractmethod
import math

class ShapeColor:
    """Класс для хранения цвета фигуры"""
    def __init__(self, color: str):
        self._color = color

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = value


class GeometricShape(ABC):
    """Абстрактный класс геометрической фигуры"""
    @abstractmethod
    def area(self) -> float:
        pass

    @classmethod
    @abstractmethod
    def shape_name(cls) -> str:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass


class Rectangle(GeometricShape):
    """Класс прямоугольника"""
    name = "Прямоугольник"

    def __init__(self, width: float, height: float, color: str):
        self.width = width
        self.height = height
        self.color_obj = ShapeColor(color)

    @property
    def color(self) -> str:
        return self.color_obj.color

    def area(self) -> float:
        return self.width * self.height

    @classmethod
    def shape_name(cls) -> str:
        return cls.name

    def get_info(self) -> str:
        return (
            "Фигура: {name}\n"
            "Ширина: {width}\n"
            "Высота: {height}\n"
            "Цвет: {color}\n"
            "Площадь: {area:.2f}"
        ).format(
            name=self.shape_name(),
            width=self.width,
            height=self.height,
            color=self.color,
            area=self.area()
        )


class Circle(GeometricShape):
    """Класс круга"""
    name = "Круг"

    def __init__(self, radius: float, color: str):
        self.radius = radius
        self.color_obj = ShapeColor(color)

    @property
    def color(self) -> str:
        return self.color_obj.color

    def area(self) -> float:
        return math.pi * self.radius ** 2

    @classmethod
    def shape_name(cls) -> str:
        return cls.name

    def get_info(self) -> str:
        return (
            "Фигура: {name}\n"
            "Радиус: {radius}\n"
            "Цвет: {color}\n"
            "Площадь: {area:.2f}"
        ).format(
            name=self.shape_name(),
            radius=self.radius,
            color=self.color,
            area=self.area()
        )