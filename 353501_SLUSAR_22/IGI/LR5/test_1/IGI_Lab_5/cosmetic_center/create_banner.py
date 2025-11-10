#!/usr/bin/env python
import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import Banner

def create_test_banner():
    print("Создание тестового баннера...")
    
    # Создаем тестовый баннер (без изображения, так как его нет)
    banner, created = Banner.objects.get_or_create(
        title="Тестовый баннер",
        defaults={
            'position': 'left',
            'order': 1,
            'is_active': True,
            'link_url': 'https://example.com'
        }
    )
    
    if created:
        print("Тестовый баннер создан!")
        print("Для добавления изображения:")
        print("1. Зайдите в админ-панель (/admin/)")
        print("2. Перейдите в 'Баннеры'")
        print("3. Отредактируйте созданный баннер")
        print("4. Загрузите изображение размером 200x300px")
    else:
        print("Тестовый баннер уже существует!")

if __name__ == '__main__':
    create_test_banner()
