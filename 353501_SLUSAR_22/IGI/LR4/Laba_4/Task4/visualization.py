import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as MplRectangle, Circle as MplCircle
from shapes import Rectangle, Circle  # Добавлен импорт классов фигур


def visualize_shape(shape, label: str):
    """Визуализация фигуры с сохранением в файл"""
    fig, ax = plt.subplots()

    if isinstance(shape, Rectangle):
        patch = MplRectangle(
            (0.1, 0.1), shape.width, shape.height,
            facecolor=shape.color,
            edgecolor='black',
            label=label
        )
        ax.set_xlim(0, shape.width * 1.2)
        ax.set_ylim(0, shape.height * 1.2)
    elif isinstance(shape, Circle):  # Явная проверка типа
        patch = MplCircle(
            (shape.radius, shape.radius), shape.radius,
            facecolor=shape.color,
            edgecolor='black',
            label=label
        )
        ax.set_xlim(0, shape.radius * 2.2)
        ax.set_ylim(0, shape.radius * 2.2)

    ax.add_patch(patch)
    ax.set_aspect('equal')
    ax.set_title(shape.shape_name())
    ax.legend()
    plt.grid(True)

    filename = f"{shape.shape_name().lower()}.png"
    plt.savefig(filename)
    print(f"\nИзображение сохранено как '{filename}'")
    plt.show()