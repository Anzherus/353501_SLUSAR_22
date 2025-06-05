# clinic/migrations/000X_add_initial_services.py
from django.db import migrations
from datetime import timedelta


def add_initial_services(apps, schema_editor):
    Service = apps.get_model('clinic', 'Service')
    DoctorSpecialization = apps.get_model('clinic', 'DoctorSpecialization')

    # Создаем специализацию если нет
    spec, _ = DoctorSpecialization.objects.get_or_create(
        name="Косметология"
    )

    services = [
        {'name': 'Консультация косметолога', 'price': 1500, 'duration': timedelta(minutes=30)},
        {'name': 'Чистка лица', 'price': 3500, 'duration': timedelta(minutes=60)},
        {'name': 'Биоревитализация', 'price': 8000, 'duration': timedelta(minutes=45)},
        {'name': 'Ботокс', 'price': 12000, 'duration': timedelta(minutes=30)},
        {'name': 'Пилинг', 'price': 4500, 'duration': timedelta(minutes=50)},
        {'name': 'Массаж лица', 'price': 3000, 'duration': timedelta(minutes=40)},
        {'name': 'Лазерная эпиляция', 'price': 5500, 'duration': timedelta(minutes=60)},
        {'name': 'Мезотерапия', 'price': 7000, 'duration': timedelta(minutes=45)},
        {'name': 'RF-лифтинг', 'price': 6500, 'duration': timedelta(minutes=50)},
        {'name': 'Плазмолифтинг', 'price': 9000, 'duration': timedelta(minutes=40)},
    ]

    for service in services:
        Service.objects.get_or_create(
            name=service['name'],
            defaults={
                'description': f"Профессиональная процедура '{service['name']}'",
                'price': service['price'],
                'duration': service['duration'],
                'specialization': spec
            }
        )


class Migration(migrations.Migration):
    dependencies = [
        ('clinic', '0002_appointment_cancellation_reason_promocode_and_more'),
    ]

    operations = [
        migrations.RunPython(add_initial_services),
    ]