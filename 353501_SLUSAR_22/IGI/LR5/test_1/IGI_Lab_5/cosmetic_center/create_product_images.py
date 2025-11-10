#!/usr/bin/env python
import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import Product

def create_product_image(product_name, price, width=300, height=300):
    """Создает изображение для товара"""
    # Создаем папку для товаров если её нет
    product_dir = 'media/products'
    os.makedirs(product_dir, exist_ok=True)
    
    # Создаем изображение
    image = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(image)
    
    # Рисуем рамку
    draw.rectangle([10, 10, width-10, height-10], outline='#8e44ad', width=3)
    
    # Добавляем текст
    try:
        title_font = ImageFont.truetype("arial.ttf", 20)
        price_font = ImageFont.truetype("arial.ttf", 16)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        price_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Название товара
    title = product_name
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    x = (width - title_width) // 2
    draw.text((x, 50), title, fill='#8e44ad', font=title_font)
    
    # Цена
    price_text = f"{price} руб."
    bbox = draw.textbbox((0, 0), price_text, font=price_font)
    price_width = bbox[2] - bbox[0]
    x = (width - price_width) // 2
    draw.text((x, 100), price_text, fill='#27ae60', font=price_font)
    
    # Декоративные элементы
    draw.ellipse([width//2-30, height//2-30, width//2+30, height//2+30], outline='#8e44ad', width=2)
    draw.text((width//2-20, height//2-10), "💄", font=small_font)
    
    # Сохраняем изображение
    filename = f"{product_name.replace(' ', '_').replace('"', '').replace('«', '').replace('»', '')}.jpg"
    image_path = os.path.join(product_dir, filename)
    image.save(image_path, 'JPEG')
    
    return f"products/{filename}"

def update_products_with_images():
    print("Создание изображений для товаров...")
    
    products = Product.objects.all()
    
    for product in products:
        print(f"Создаем изображение для: {product.name}")
        
        # Создаем изображение
        image_path = create_product_image(product.name, product.price)
        
        # Обновляем товар
        product.image = image_path
        product.save()
        
        print(f"✅ Изображение создано: {image_path}")
    
    print(f"\n✅ Всего обновлено товаров: {products.count()}")

if __name__ == '__main__':
    try:
        update_products_with_images()
    except ImportError:
        print("PIL не установлен. Устанавливаем...")
        os.system("pip install Pillow")
        print("Попробуйте запустить скрипт снова.")
