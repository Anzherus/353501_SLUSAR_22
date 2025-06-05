from parallelogram import Parallelogram
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np


def input_float(prompt, min_val=0):
    """Ввод числа с проверкой корректности"""
    while True:
        try:
            value = float(input(prompt))
            if value <= min_val:
                print(f"Значение должно быть больше {min_val}")
                continue
            return value
        except ValueError:
            print("Пожалуйста, введите число")


def calculate_parallelogram_vertices(d1, d2, angle_deg):
    """Вычисляет координаты вершин параллелограмма по диагоналям и углу"""
    angle_rad = np.radians(angle_deg)

    # Половины диагоналей
    a = d1 / 2
    b = d2 / 2

    # Вычисляем координаты вершин
    p1 = np.array([a, 0])
    p2 = np.array([-a, 0])
    p3 = np.array([b * np.cos(angle_rad), b * np.sin(angle_rad)])
    p4 = np.array([-b * np.cos(angle_rad), -b * np.sin(angle_rad)])

    # Вершины параллелограмма (точки пересечения диагоналей + векторы)
    v1 = p1 + p3
    v2 = p1 + p4
    v3 = p2 + p4
    v4 = p2 + p3

    return [v1, v2, v3, v4]


def main():
    print("Создание параллелограмма")

    # 1. Ввод параметров
    d1 = input_float("Введите первую диагональ (d1): ")
    d2 = input_float("Введите вторую диагональ (d2): ")
    angle = input_float("Введите угол между диагоналями (в градусах, 0-180): ", 0)
    if angle >= 180:
        print("Угол должен быть меньше 180 градусов")
        return

    color = input("Введите цвет фигуры: ")
    label = input("Введите подпись для фигуры: ")

    # 2. Создание параллелограмма
    parallelogram = Parallelogram(d1, d2, angle, color)

    # Вывод информации о фигуре
    print("\nСозданная фигура:")
    print(parallelogram.get_parameters())

    # 3-4. Визуализация фигуры
    fig, ax = plt.subplots()

    # Вычисляем вершины параллелограмма
    vertices = calculate_parallelogram_vertices(d1, d2, angle)

    # Создаем полигон параллелограмма
    parallelogram_polygon = patches.Polygon(
        vertices,
        closed=True,
        linewidth=2,
        edgecolor='black',
        facecolor=parallelogram.color
    )
    ax.add_patch(parallelogram_polygon)

    # Добавляем подпись (в центре фигуры)
    center_x = sum(v[0] for v in vertices) / 4
    center_y = sum(v[1] for v in vertices) / 4
    ax.text(center_x, center_y, label,
            ha='center', va='center',
            fontsize=12, color='white')

    # Настраиваем границы отображения
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]
    ax.set_xlim(min(all_x) - 1, max(all_x) + 1)
    ax.set_ylim(min(all_y) - 1, max(all_y) + 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(f"Параллелограмм ({parallelogram.color})")

    # Сохраняем в файл
    filename = "parallelogram.png"
    plt.savefig(filename)
    print(f"\nФигура сохранена в файл {filename}")

    # Показываем фигуру
    plt.show()


if __name__ == "__main__":
    main()