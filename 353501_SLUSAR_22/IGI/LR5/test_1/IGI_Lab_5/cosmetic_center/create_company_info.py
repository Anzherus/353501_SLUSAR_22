#!/usr/bin/env python
import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import CompanyInfo

def create_company_logo():
    """Creates test company logo"""
    # Create logo directory if it doesn't exist
    logo_dir = 'media/company'
    os.makedirs(logo_dir, exist_ok=True)
    
    # Create image 300x150px
    width, height = 300, 150
    image = Image.new('RGB', (width, height), color='#8e44ad')
    draw = ImageDraw.Draw(image)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Draw text
    text = "ЭСТЕТИКА"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Save image
    image_path = os.path.join(logo_dir, 'logo.jpg')
    image.save(image_path, 'JPEG')
    
    return image_path

def create_company_certificate():
    """Creates test certificate"""
    # Create certificate directory if it doesn't exist
    cert_dir = 'media/company'
    os.makedirs(cert_dir, exist_ok=True)
    
    # Create image 400x300px
    width, height = 400, 300
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw border
    draw.rectangle([10, 10,width-10, height-10], outline='black', width=3)
    
    # Add text
    try:
        title_font = ImageFont.truetype("arial.ttf", 20)
        text_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Title
    title = "СЕРТИФИКАТ"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    x = (width - title_width) // 2
    draw.text((x, 50), title, fill='black', font=title_font)
    
    # Certificate text
    text_lines = [
        "Косметологический Центр",
        "«ЭСТЕТИКА»",
        "",
        "Сертифицирован для оказания",
        "косметологических услуг",
        "",
        "Дата выдачи: 2024"
    ]
    
    y = 100
    for line in text_lines:
        if line:
            bbox = draw.textbbox((0, 0), line, font=text_font)
            line_width = bbox[2] - bbox[0]
            x = (width - line_width) // 2
            draw.text((x, y), line, fill='black', font=text_font)
        y += 25
    
    # Save image
    image_path = os.path.join(cert_dir, 'certificate.jpg')
    image.save(image_path, 'JPEG')
    
    return image_path

def create_company_info():
    print("Creating company information...")
    
    # Create logo and certificate
    logo_path = create_company_logo()
    cert_path = create_company_certificate()
    
    print(f"Logo created: {logo_path}")
    print(f"Certificate created: {cert_path}")
    
    # Create company information
    company_info, created = CompanyInfo.objects.get_or_create(
        name="Косметологический Центр «Эстетика»",
        defaults={
            'description': '''
            Добро пожаловать в Косметологический Центр «Эстетика» — место, где красота встречается с профессионализмом. 
            Наш центр специализируется на предоставлении высококачественных косметологических услуг с использованием 
            современных технологий и проверенных методик.
            
            Мы работаем с 2015 года и за это время помогли тысячам клиентов обрести уверенность в себе и улучшить 
            качество своей кожи. Наша команда состоит из опытных специалистов, которые постоянно совершенствуют 
            свои навыки и следят за новейшими тенденциями в области косметологии.
            ''',
            'history': '''
            2015 - Открытие центра «Эстетика» с командой из 3 специалистов
            2017 - Расширение услуг, добавление аппаратной косметологии
            2019 - Открытие второго филиала в центре города
            2021 - Внедрение новейших лазерных технологий
            2023 - Получение сертификата международного стандарта
            2024 - Запуск онлайн-записи и мобильного приложения
            ''',
            'requisites': '''
            Косметологический Центр «Эстетика»
            УНП: 123456789
            Адрес: г. Минск, ул. Космонавтов, 15
            Телефон: +375 (29) 123-45-67
            Email: info@estetika.by
            Сайт: www.estetika.by
            
            Режим работы:
            Пн-Пт: 9:00 - 21:00
            Сб-Вс: 10:00 - 18:00
            ''',
             'video_url': '',  # Оставляем пустым для использования локального файла
             'video_file': '',  # Будет заполнено позже
            'logo': 'company/logo.jpg',
            'certificate': 'company/certificate.jpg'
        }
    )
    
    if created:
        print("Company information created!")
    else:
        print("Company information already exists!")
        # Update logo and certificate
        company_info.logo = 'company/logo.jpg'
        company_info.certificate = 'company/certificate.jpg'
        company_info.save()
        print("Logo and certificate updated!")

if __name__ == '__main__':
    try:
        create_company_info()
    except ImportError:
        print("PIL not installed. Installing...")
        os.system("pip install Pillow")
        print("Please try running the script again.")
