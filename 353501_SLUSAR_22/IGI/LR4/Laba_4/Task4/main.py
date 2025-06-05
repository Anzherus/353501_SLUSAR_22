from shapes import Rectangle, Circle
from input_utils import input_float, input_shape_choice
from visualization import visualize_shape


def create_rectangle():
    """Создание прямоугольника"""
    print("\nСоздание прямоугольника")
    width = input_float("Введите ширину: ")
    height = input_float("Введите высоту: ")
    color = input("Введите цвет (англ.): ")
    label = input("Введите подпись: ")
    return Rectangle(width, height, color), label


def create_circle():
    """Создание круга"""
    print("\nСоздание круга")
    radius = input_float("Введите радиус: ")
    color = input("Введите цвет (англ.): ")
    label = input("Введите подпись: ")
    return Circle(radius, color), label


def main():
    print("=== Программа для работы с геометрическими фигурами ===")

    while True:
        choice = input_shape_choice()

        if choice == '0':
            print("\nПрограмма завершена.")
            break
        elif choice == '1':
            shape, label = create_rectangle()
        elif choice == '2':
            shape, label = create_circle()
        else:
            print("Некорректный выбор. Попробуйте снова.")
            continue

        print("\n" + shape.get_info())
        visualize_shape(shape, label)


if __name__ == "__main__":
    main()