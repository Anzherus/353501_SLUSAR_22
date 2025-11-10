#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import Product, ProductCategory

def check_products():
    print("Проверка товаров в базе данных...")
    
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    
    print(f"Категорий товаров: {categories.count()}")
    for category in categories:
        print(f"  - {category.name} (активна: {category.is_active})")
    
    print(f"\nТоваров: {products.count()}")
    for product in products:
        print(f"  - {product.name} (активен: {product.is_active}, цена: {product.price})")
    
    active_products = Product.objects.filter(is_active=True)
    print(f"\nАктивных товаров: {active_products.count()}")
    
    if active_products.count() == 0:
        print("\n⚠️  Нет активных товаров! Создаем тестовые товары...")
        from create_test_data import create_test_data
        create_test_data()
        print("✅ Тестовые товары созданы!")

if __name__ == '__main__':
    check_products()
