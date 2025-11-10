#!/usr/bin/env python
import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import Partner

def create_partner_logo(partner_name, width=200, height=100):
    """Создает логотип для партнера"""
    # Создаем папку для логотипов партнеров если её нет
    partner_dir = 'media/partners'
    os.makedirs(partner_dir, exist_ok=True)
    
    # Создаем изображение
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Рисуем рамку
    draw.rectangle([5, 5, width-5, height-5], outline='#8e44ad', width=2)
    
    # Добавляем текст
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Рисуем текст
    text = partner_name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill='#8e44ad', font=font)
    
    # Сохраняем изображение
    filename = f"{partner_name.replace(' ', '_').replace('«', '').replace('»', '')}.jpg"
    image_path = os.path.join(partner_dir, filename)
    image.save(image_path, 'JPEG')
    
    return f"partners/{filename}"

def create_partners():
    print("Создание партнеров...")
    
    partners_data = [
        {
            'name': 'L\'Oréal Paris',
            'description': 'Ведущий мировой бренд косметики и парфюмерии',
            'website_url': 'https://www.loreal-paris.ru/',
            'order': 1
        },
        {
            'name': 'Estée Lauder',
            'description': 'Премиальная косметика и средства по уходу за кожей',
            'website_url': 'https://www.esteelauder.ru/',
            'order': 2
        },
        {
            'name': 'Clinique',
            'description': 'Дерматологически протестированная косметика',
            'website_url': 'https://www.clinique.ru/',
            'order': 3
        },
        {
            'name': 'La Roche-Posay',
            'description': 'Французская дерматологическая косметика',
            'website_url': 'https://www.laroche-posay.ru/',
            'order': 4
        },
        {
            'name': 'Vichy',
            'description': 'Французская косметика с термальной водой',
            'website_url': 'https://www.vichy.ru/',
            'order': 5
        },
        {
            'name': 'Avene',
            'description': 'Французская дерматологическая косметика',
            'website_url': 'https://www.avene.ru/',
            'order': 6
        }
    ]
    
    for partner_data in partners_data:
        print(f"Создаем партнера: {partner_data['name']}")
        
        # Создаем логотип
        logo_path = create_partner_logo(partner_data['name'])
        
        # Создаем партнера в базе данных
        partner, created = Partner.objects.get_or_create(
            name=partner_data['name'],
            defaults={
                'description': partner_data['description'],
                'website_url': partner_data['website_url'],
                'order': partner_data['order'],
                'is_active': True,
                'logo': logo_path
            }
        )
        
        if created:
            print(f"✅ Партнер создан: {partner.name}")
        else:
            print(f"⚠️  Партнер уже существует: {partner.name}")
            # Обновляем логотип если партнер уже существует
            partner.logo = logo_path
            partner.save()
            print(f"✅ Логотип обновлен для: {partner.name}")
    
    print(f"\n✅ Всего партнеров: {Partner.objects.count()}")

if __name__ == '__main__':
    try:
        create_partners()
    except ImportError:
        print("PIL не установлен. Устанавливаем...")
        os.system("pip install Pillow")
        print("Попробуйте запустить скрипт снова.")
