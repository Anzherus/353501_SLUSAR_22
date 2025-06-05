import pandas as pd
from IPython.display import display

def main():
    # 1. Импорт библиотеки и загрузка данных
    print("1. Библиотека Pandas. Импорт библиотеки.")
    try:
        df = pd.read_csv('train.csv')
        print("Данные успешно загружены!")
    except FileNotFoundError:
        print("Файл не найден. Пожалуйста, скачайте датасет Titanic с Kaggle.")
        return

    # 2-3. Структура Series и создание Series
    print("\n2-3. Структура Series. Создание Series.")
    ages = df['Age']
    print("Пример Series (возраст пассажиров):")
    display(ages.head())

    # 4. Функция display
    print("\n4. Функция display")
    custom_series = pd.Series([10, 20, 30, 40, 50],
                            index=['a', 'b', 'c', 'd', 'e'],
                            name='Пример Series')
    display(custom_series)

    # 5. Доступ к элементам Series
    print("\n5. Доступ к элементам Series с использованием .loc или .iloc")
    print("По индексу (iloc):", custom_series.iloc[2])
    print("По метке (loc):", custom_series.loc['c'])

    # 6. Объект DataFrame. Создание.
    print("\n6. Объект DataFrame. Создание.")
    print("Датасет Titanic:")
    display(df.head())

    data = {
        'Имя': ['Анна', 'Борис', 'Виктор', 'Галина'],
        'Возраст': [25, 32, 37, 19],
        'Город': ['Москва', 'Санкт-Петербург', 'Казань', 'Владивосток']
    }
    custom_df = pd.DataFrame(data)
    print("\nСозданный вручную DataFrame:")
    display(custom_df)

if __name__ == "__main__":
    main()
    # Анализ данных Titanic
    print("\nДополнительный анализ данных Titanic:")
    print("\nИнформация о датафрейме:")
    print(df.info())

    print("\nОписательная статистика:")
    display(df.describe())

    print("\nКоличество выживших по классам:")
    display(df.groupby('Pclass')['Survived'].mean())
