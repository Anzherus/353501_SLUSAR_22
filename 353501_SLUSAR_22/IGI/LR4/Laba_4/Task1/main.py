"""
Программа для учета школьников

Эта программа управляет данными учащихся (фамилия, возраст) с сериализацией в CSV и pickle.
Позволяет группировать учеников по возрастным категориям и искать конкретных учеников.

Лабораторная работа: 1
Название: Система учета школьников
Версия: 1.0
Разработчик: Слюсарь Станислав Юрьевич
Дата: 15.04.2025
"""

import csv
import pickle
from abc import ABC, abstractmethod
from typing import List, Dict, Union


class DataSerializer(ABC):
    """Абстрактный базовый класс для сериализации данных"""
    
    @abstractmethod
    def save(self, data: List[Dict], filename: str) -> None:
        """Сохранить данные в файл"""
        pass
    
    @abstractmethod
    def load(self, filename: str) -> List[Dict]:
        """Загрузить данные из файла"""
        pass


class CSVSerializer(DataSerializer):
    """Реализация для CSV сериализации"""
    
    def save(self, data: List[Dict], filename: str) -> None:
        """Сохранить данные в CSV файл"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except (IOError, csv.Error) as e:
            raise ValueError(f"Ошибка сохранения CSV: {str(e)}")
    
    def load(self, filename: str) -> List[Dict]:
        """Загрузить данные из CSV файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except (IOError, csv.Error) as e:
            raise ValueError(f"Ошибка загрузки CSV: {str(e)}")


class PickleSerializer(DataSerializer):
    """Реализация для pickle сериализации"""
    
    def save(self, data: List[Dict], filename: str) -> None:
        """Сохранить данные с помощью pickle"""
        try:
            with open(filename, 'wb') as file:
                pickle.dump(data, file)
        except (pickle.PickleError, IOError) as e:
            raise ValueError(f"Ошибка сохранения pickle: {str(e)}")
    
    def load(self, filename: str) -> List[Dict]:
        """Загрузить данные с помощью pickle"""
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except (pickle.PickleError, IOError, EOFError) as e:
            raise ValueError(f"Ошибка загрузки pickle: {str(e)}")


class AgeGroupMixin:
    """Миксин для функциональности возрастных групп"""
    
    def get_age_groups(self, students: List[Dict]) -> Dict[str, List[Dict]]:
        """Группировать учеников по возрастным категориям"""
        groups = {
            "7-10 лет": [],
            "11-13 лет": [],
            "14-16 лет": [],
            "17-18 лет": []
        }
        
        for student in students:
            try:
                age = int(student['age'])
                if 7 <= age <= 10:
                    groups["7-10 лет"].append(student)
                elif 11 <= age <= 13:
                    groups["11-13 лет"].append(student)
                elif 14 <= age <= 16:
                    groups["14-16 лет"].append(student)
                elif 17 <= age <= 18:
                    groups["17-18 лет"].append(student)
            except (KeyError, ValueError):
                continue
        
        return groups


class StudentManager(AgeGroupMixin):
    """Основной класс для управления учениками"""
    
    def __init__(self, serializer: DataSerializer):
        self.serializer = serializer
        self._students = []  # Защищенный атрибут
        
    @property
    def students(self) -> List[Dict]:
        """Геттер для списка учеников"""
        return self._students
    
    @students.setter
    def students(self, value: List[Dict]) -> None:
        """Сеттер для списка учеников с валидацией"""
        if not isinstance(value, list):
            raise ValueError("Ученики должны быть списком словарей")
        self._students = value
    
    def add_student(self, last_name: str, age: int) -> None:
        """Добавить нового ученика в список"""
        try:
            age_int = int(age)
            if age_int < 7 or age_int > 18:
                raise ValueError("Возраст должен быть от 7 до 18 лет")
            self._students.append({"last_name": last_name, "age": str(age_int)})
        except ValueError as e:
            raise ValueError(f"Некорректный возраст: {str(e)}")
    
    def find_student(self, last_name: str) -> Union[Dict, None]:
        """Найти ученика по фамилии (без учета регистра)"""
        for student in self._students:
            if student['last_name'].lower() == last_name.lower():
                return student
        return None
    
    def sort_students(self, by: str = 'last_name') -> None:
        """Сортировать учеников по указанному полю"""
        if not self._students:
            return
            
        if by not in self._students[0].keys():
            raise ValueError(f"Невозможно сортировать по '{by}' - поле не существует")
            
        self._students.sort(key=lambda x: x[by])
    
    def save_to_file(self, filename: str) -> None:
        """Сохранить учеников в файл с помощью выбранного сериализатора"""
        if not self._students:
            raise ValueError("Нет учеников для сохранения")
        self.serializer.save(self._students, filename)
    
    def load_from_file(self, filename: str) -> None:
        """Загрузить учеников из файла с помощью выбранного сериализатора"""
        self._students = self.serializer.load(filename)
        
        # Проверка загруженных данных
        for student in self._students:
            if 'last_name' not in student or 'age' not in student:
                raise ValueError("Некорректная структура данных ученика в файле")


class UserInterface:
    """Класс для взаимодействия с пользователем"""
    
    @staticmethod
    def display_menu() -> None:
        """Отобразить меню"""
        print("\nСистема учета школьников")
        print("1. Добавить нового ученика")
        print("2. Найти ученика по фамилии")
        print("3. Показать всех учеников")
        print("4. Показать учеников по возрастным группам")
        print("5. Сортировать учеников")
        print("6. Сохранить данные в файл")
        print("7. Загрузить данные из файла")
        print("8. Выход")
    
    @staticmethod
    def get_choice() -> int:
        """Получить выбор пользователя с валидацией"""
        while True:
            try:
                choice = int(input("Введите номер пункта (1-8): "))
                if 1 <= choice <= 8:
                    return choice
                print("Пожалуйста, введите число от 1 до 8")
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите число")
    
    @staticmethod
    def get_student_info() -> tuple:
        """Получить информацию об ученике от пользователя"""
        while True:
            last_name = input("Введите фамилию ученика: ").strip()
            if last_name:
                break
            print("Фамилия не может быть пустой")
        
        while True:
            age = input("Введите возраст ученика (7-18): ").strip()
            try:
                age_int = int(age)
                if 7 <= age_int <= 18:
                    break
                print("Возраст должен быть от 7 до 18 лет")
            except ValueError:
                print("Возраст должен быть числом")
        
        return last_name, age_int
    
    @staticmethod
    def get_search_name() -> str:
        """Получить фамилию для поиска"""
        return input("Введите фамилию для поиска: ").strip()
    
    @staticmethod
    def display_student(student: Dict) -> None:
        """Отобразить информацию об ученике"""
        if student:
            print(f"\nНайден ученик: Фамилия: {student['last_name']}, Возраст: {student['age']}")
        else:
            print("\nУченик не найден")
    
    @staticmethod
    def display_all_students(students: List[Dict]) -> None:
        """Отобразить всех учеников"""
        if not students:
            print("\nВ системе нет учеников")
            return
        
        print("\nСписок всех учеников:")
        for idx, student in enumerate(students, 1):
            print(f"{idx}. {student['last_name']}, {student['age']} лет")
    
    @staticmethod
    def display_age_groups(groups: Dict[str, List[Dict]]) -> None:
        """Отобразить учеников по возрастным группам"""
        if not any(groups.values()):
            print("\nНет учеников ни в одной возрастной группе")
            return
        
        print("\nУченики по возрастным группам:")
        for group, students in groups.items():
            print(f"\n{group}:")
            if students:
                for student in students:
                    print(f"- {student['last_name']} ({student['age']} лет)")
            else:
                print("Нет учеников в этой группе")
    
    @staticmethod
    def get_sort_field() -> str:
        """Получить поле для сортировки"""
        while True:
            field = input("Введите поле для сортировки (фамилия/возраст): ").strip().lower()
            if field in ('фамилия', 'возраст'):
                return 'last_name' if field == 'фамилия' else 'age'
            print("Некорректное поле. Введите 'фамилия' или 'возраст'")
    
    @staticmethod
    def get_filename() -> str:
        """Получить имя файла от пользователя"""
        while True:
            filename = input("Введите имя файла: ").strip()
            if filename:
                return filename
            print("Имя файла не может быть пустым")
    
    @staticmethod
    def get_serializer_choice() -> DataSerializer:
        """Получить выбор формата сериализации"""
        while True:
            choice = input("Выберите формат (1 - CSV, 2 - Pickle): ").strip()
            if choice == '1':
                return CSVSerializer()
            elif choice == '2':
                return PickleSerializer()
            print("Пожалуйста, введите 1 или 2")


def main():
    """Основная функция программы"""
    # Инициализация с сериализатором  
    manager = StudentManager(CSVSerializer())
    ui = UserInterface()
    
    while True:
        ui.display_menu()
        choice = ui.get_choice()
        
        try:
            if choice == 1:  # Добавить ученика
                last_name, age = ui.get_student_info()
                manager.add_student(last_name, age)
                print("Ученик успешно добавлен")
            
            elif choice == 2:  # Найти ученика
                if not manager.students:
                    print("В системе нет учеников")
                    continue
                last_name = ui.get_search_name()
                student = manager.find_student(last_name)
                ui.display_student(student)
            
            elif choice == 3:  # Показать всех учеников
                ui.display_all_students(manager.students)
            
            elif choice == 4:  # Показать возрастные группы
                groups = manager.get_age_groups(manager.students)
                ui.display_age_groups(groups)
            
            elif choice == 5:  # Сортировать учеников
                if not manager.students:
                    print("Нет учеников для сортировки")
                    continue
                field = ui.get_sort_field()
                manager.sort_students(field)
                print("Ученики успешно отсортированы")
                ui.display_all_students(manager.students)
            
            elif choice == 6:  # Сохранить в файл
                if not manager.students:
                    print("Нет учеников для сохранения")
                    continue
                print("Выберите формат файла:")
                manager.serializer = ui.get_serializer_choice()
                filename = ui.get_filename()
                manager.save_to_file(filename)
                print("Данные успешно сохранены")
            
            elif choice == 7:  # Загрузить из файла
                print("Выберите формат файла:")
                manager.serializer = ui.get_serializer_choice()
                filename = ui.get_filename()
                manager.load_from_file(filename)
                print("Данные успешно загружены")
                ui.display_all_students(manager.students)
            
            elif choice == 8:  # Выход
                print("До свидания!")
                break
        
        except Exception as e:
            print(f"\nОшибка: {str(e)}")
        
        # Запрос на продолжение
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()