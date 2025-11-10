#!/usr/bin/env python
import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import Banner

def create_test_banner_image():
    """Создает тестовое изображение для баннера"""
    # Создаем папку для баннеров если её нет
    banner_dir = 'media/banners'
    os.makedirs(banner_dir, exist_ok=True)
    
    # Создаем изображение 200x300px
    width, height = 200, 300
    image = Image.new('RGB', (width, height), color='#8e44ad')
    draw = ImageDraw.Draw(image)
    
    # Добавляем текст
    try:
        # Пытаемся использовать системный шрифт
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        # Если не получается, используем стандартный
        font = ImageFont.load_default()
    
    # Рисуем текст
    text = "РЕКЛАМА\nКОСМЕТИКИ"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font, align='center')
    
    # Сохраняем изображение
    image_path = os.path.join(banner_dir, 'test_banner.jpg')
    image.save(image_path, 'JPEG')
    
    return image_path

def create_test_banner():
    print("Создание тестового баннера с изображением...")
    
    # Создаем тестовое изображение
    image_path = create_test_banner_image()
    print(f"Изображение создано: {image_path}")
    
    # Создаем баннер в базе данных
    banner, created = Banner.objects.get_or_create(
        title="Тестовый баннер",
        defaults={
            'position': 'left',
            'order': 1,
            'is_active': True,
            'link_url': 'https://example.com',
            'image': 'banners/test_banner.jpg'
        }
    )
    
    if created:
        print("Тестовый баннер создан в базе данных!")
    else:
        print("Тестовый баннер уже существует!")
        # Обновляем изображение если баннер уже существует
        banner.image = 'banners/test_banner.jpg'
        banner.save()
        print("Изображение обновлено!")

if __name__ == '__main__':
    try:
        create_test_banner()
    except ImportError:
        print("PIL не установлен. Устанавливаем...")
        os.system("pip install Pillow")
        print("Попробуйте запустить скрипт снова.")
