#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import Review, Client, Doctor, User
from django.contrib.auth.models import User

def test_review_creation():
    print("Тестирование создания отзыва...")
    
    # Создаем тестового пользователя если его нет
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print("✅ Создан тестовый пользователь")
    
    # Создаем профиль клиента если его нет
    try:
        client = user.client
    except Client.DoesNotExist:
        client = Client.objects.create(
            user=user,
            phone='+7-999-999-99-99',
            birth_date='1990-01-01'
        )
        print("✅ Создан профиль клиента")
    
    # Получаем первого врача
    try:
        doctor = Doctor.objects.first()
        if not doctor:
            print("⚠️  Нет врачей в базе данных")
            doctor = None
    except:
        doctor = None
    
    # Создаем тестовый отзыв
    try:
        review = Review.objects.create(
            client=client,
            rating=5,
            text='Тестовый отзыв для проверки функциональности',
            doctor=doctor
        )
        print(f"✅ Отзыв создан: {review}")
        print(f"   - Клиент: {review.client}")
        print(f"   - Врач: {review.doctor}")
        print(f"   - Оценка: {review.rating}")
        print(f"   - Текст: {review.text[:50]}...")
        
        # Удаляем тестовый отзыв
        review.delete()
        print("✅ Тестовый отзыв удален")
        
    except Exception as e:
        print(f"❌ Ошибка при создании отзыва: {e}")
        return False
    
    return True

def test_review_form():
    print("\nТестирование формы отзыва...")
    
    from clinic.forms import ReviewForm
    
    # Тестируем валидную форму
    form_data = {
        'rating': '5',
        'text': 'Отличный сервис!',
        'doctor': ''
    }
    
    form = ReviewForm(data=form_data)
    if form.is_valid():
        print("✅ Форма валидна")
        print(f"   - Оценка: {form.cleaned_data['rating']}")
        print(f"   - Текст: {form.cleaned_data['text']}")
        print(f"   - Врач: {form.cleaned_data.get('doctor')}")
    else:
        print("❌ Форма невалидна:")
        for field, errors in form.errors.items():
            print(f"   - {field}: {errors}")
    
    # Тестируем невалидную форму
    form_data_invalid = {
        'rating': '',
        'text': '',
        'doctor': ''
    }
    
    form_invalid = ReviewForm(data=form_data_invalid)
    if not form_invalid.is_valid():
        print("✅ Невалидная форма правильно отклонена")
    else:
        print("❌ Невалидная форма была принята")

if __name__ == '__main__':
    print("🔍 Тестирование функциональности отзывов\n")
    
    try:
        # Тест создания отзыва
        if test_review_creation():
            print("\n✅ Тест создания отзыва прошел успешно")
        else:
            print("\n❌ Тест создания отзыва не прошел")
        
        # Тест формы
        test_review_form()
        
        print("\n🎉 Все тесты завершены!")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
