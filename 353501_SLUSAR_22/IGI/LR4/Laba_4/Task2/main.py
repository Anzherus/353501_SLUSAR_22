
import re
import zipfile
import os
from collections import defaultdict

def main():
    # 1. Чтение входного файла
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("Ошибка: файл input.txt не найден!")
        print("Создайте файл input.txt с текстом для анализа в той же папке, где находится программа.")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    if not text:
        print("Файл input.txt пуст!")
        return

    # 2. Анализ текста
    # Разделение на предложения
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    
    # Извлечение слов
    words = re.findall(r'\b[а-яА-ЯёЁa-zA-Z]+\b', text)
    
    # Поиск email
    emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
    
    # Поиск смайликов
    smiles = []
    for match in re.finditer(r'[:;]-*[()[\]]+', text):
        smile = match.group()
        if len(smile) > 1 and smile[-1] in '()[]':
            smiles.append(smile)
    
    # Подсчет статистики
    stats = {

        'total_sentences': len(sentences),
        'sentence_types': {
            'повествовательные': sum(1 for s in sentences if s.endswith('.')),
            'вопросительные': sum(1 for s in sentences if s.endswith('?')),
            'побудительные': sum(1 for s in sentences if s.endswith('!'))
        },
        'avg_sentence_length': round(sum(len(s.split()) for s in sentences)/len(sentences), 2) if sentences else 0,
        'avg_word_length': round(sum(len(w) for w in words)/len(words), 2) if words else 0,
        'smiles_count': len(smiles),
        'emails': emails,
        'vowel_words': sum(1 for w in words if w[0].lower() in 'аеёиоуыэюяaeiou' or w[-1].lower() in 'аеёиоуыэюяaeiou'),
        'words_after_comma': sorted(set(
            word.lower() for s in sentences 
            for part in s.split(',')[1:] 
            for word in re.findall(r'[а-яА-ЯёЁa-zA-Z]+', part.strip())
        )),
        'modified_text': re.sub(r'\$v_\(([a-z0-9])\)\$', r'v[\1]', text)
    }

    # 3. Сохранение результатов
    try:
        with open('result.txt', 'w', encoding='utf-8') as f:
            f.write("АНАЛИЗ ТЕКСТА\n")
            f.write("="*50 + "\n\n")
            f.write(f"1. Всего предложений: {stats['total_sentences']}\n\n")
            
            f.write("2. Типы предложений:\n")
            for typ, count in stats['sentence_types'].items():
                f.write(f"   - {typ}: {count}\n")
            f.write("\n")
            
            f.write(f"3. Средняя длина предложения: {stats['avg_sentence_length']} слов\n")
            f.write(f"4. Средняя длина слова: {stats['avg_word_length']} букв\n")
            f.write(f"5. Найдено смайликов: {stats['smiles_count']}\n\n")
            
            f.write("6. Email адреса:\n")
            for email in stats['emails']:
                f.write(f"   - {email}\n")
            f.write("\n")
            
            f.write(f"7. Слов на гласные: {stats['vowel_words']}\n\n")
            
            f.write("8. Слова после запятых:\n")
            for word in stats['words_after_comma']:
                f.write(f"   - {word}\n")
            f.write("\n")
            
            f.write("9. Модифицированный текст:\n")
            f.write(stats['modified_text'])
        
        print("Результаты сохранены в result.txt")
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")
        return

    # 4. Архивирование
    try:
        with zipfile.ZipFile('result.zip', 'w') as z:
            z.write('result.txt')
        print("Архив создан: result.zip")
    except Exception as e:
        print(f"Ошибка при создании архива: {e}")

if __name__ == "__main__":
    main()
    input("\nНажмите Enter для выхода...")