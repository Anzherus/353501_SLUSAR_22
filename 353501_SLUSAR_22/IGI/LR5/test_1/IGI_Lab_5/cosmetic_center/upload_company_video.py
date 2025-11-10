#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import CompanyInfo

def upload_company_video(video_path):
    """
    Загружает видео файл для компании
    
    Args:
        video_path (str): Путь к MP4 файлу
    """
    if not os.path.exists(video_path):
        print(f"❌ Файл не найден: {video_path}")
        return False
    
    # Проверяем расширение файла
    if not video_path.lower().endswith('.mp4'):
        print("❌ Файл должен иметь расширение .mp4")
        return False
    
    try:
        # Создаем папку для видео если её нет
        videos_dir = 'media/company/videos'
        os.makedirs(videos_dir, exist_ok=True)
        
        # Получаем или создаем информацию о компании
        company_info, created = CompanyInfo.objects.get_or_create(
            name="Косметологический Центр «Эстетика»",
            defaults={
                'name': "Косметологический Центр «Эстетика»",
                'description': "Описание компании будет добавлено позже.",
                'history': "История компании будет добавлена позже.",
                'requisites': "Реквизиты будут добавлены позже.",
                'logo': '',
                'certificate': ''
            }
        )
        
        # Копируем видео файл
        import shutil
        video_filename = os.path.basename(video_path)
        dest_path = os.path.join(videos_dir, video_filename)
        
        # Если файл уже существует, добавляем номер
        counter = 1
        original_dest_path = dest_path
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(original_dest_path)
            dest_path = f"{name}_{counter}{ext}"
            counter += 1
        
        shutil.copy2(video_path, dest_path)
        
        # Обновляем информацию о компании
        relative_path = f'company/videos/{os.path.basename(dest_path)}'
        company_info.video_file = relative_path
        company_info.video_url = ''  # Очищаем URL чтобы использовать локальный файл
        company_info.save()
        
        print("✅ Видео успешно загружено!")
        print(f"📁 Файл сохранен: {dest_path}")
        print(f"🎥 Видео будет отображаться на странице 'О нас'")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке видео: {str(e)}")
        return False

def main():
    """
    Интерактивная загрузка видео
    """
    print("=== Загрузка видео для компании ===")
    print()
    
    while True:
        video_path = input("Введите путь к MP4 файлу (или 'exit' для выхода): ").strip()
        
        if video_path.lower() == 'exit':
            print("Выход...")
            break
        
        if not video_path:
            print("❌ Путь не может быть пустым")
            continue
        
        # Убираем кавычки если они есть
        video_path = video_path.strip('"').strip("'")
        
        print(f"\n📁 Загружаем видео: {video_path}")
        
        if upload_company_video(video_path):
            print("\n🎉 Видео загружено успешно!")
            print("Откройте сайт и перейдите на страницу 'О нас' чтобы увидеть результат.")
            
            response = input("\nЗагрузить ещё одно видео? (y/n): ").strip().lower()
            if response != 'y':
                break
        else:
            print("\n❌ Не удалось загрузить видео. Попробуйте ещё раз.")

if __name__ == '__main__':
    main()
