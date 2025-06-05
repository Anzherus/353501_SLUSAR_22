from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date


class DoctorSpecialization(models.Model):
    # Модель специализации врача
    name = models.CharField(max_length=100)  # Название специализации, максимум 100 символов

    def __str__(self):
        return self.name


class Doctor(models.Model):
    # Модель врача
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один-к-одному с пользователем
    specialization = models.ForeignKey(DoctorSpecialization, on_delete=models.SET_NULL, null=True)  # Связь со специализацией
    bio = models.TextField()  # Биография врача
    photo = models.ImageField(upload_to='doctors/')  # Фото врача
    experience = models.PositiveIntegerField()  # Опыт работы (только положительные числа)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialization})"


class Service(models.Model):
    # Модель услуги
    name = models.CharField(max_length=200)  # Название услуги, максимум 200 символов
    description = models.TextField()  # Описание услуги
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена услуги
    duration = models.DurationField()  # Длительность услуги
    specialization = models.ForeignKey(DoctorSpecialization, on_delete=models.SET_NULL, null=True)  # Связь со специализацией

    def __str__(self):
        return self.name


class Client(models.Model):
    # Модель клиента
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один-к-одному с пользователем
    phone = models.CharField(max_length=20)  # Телефон, максимум 20 символов
    birth_date = models.DateField()  # Дата рождения
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', verbose_name="Пол")  # Пол с предопределенными значениями

    def __str__(self):
        return self.user.get_full_name()

    def clean(self):
        # Валидация возраста клиента на уровне модели
        super().clean()
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        if age < 18:
            raise ValidationError({'birth_date': 'Клиент должен быть старше 18 лет.'})


class Review(models.Model):
    # Модель отзыва
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Связь с клиентом
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')  # Связь с врачом
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Оценка от 1 до 5
    text = models.TextField()  # Текст отзыва
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания отзыва

    def __str__(self):
        return f"Отзыв от {self.client} ({self.rating}/5) для {self.doctor}"


class PromoCode(models.Model):
    # Модель промокода
    name = models.CharField(max_length=100)  # Название промокода, максимум 100 символов
    code = models.CharField(max_length=20, unique=True)  # Уникальный код промокода
    discount = models.PositiveIntegerField(help_text="Процент скидки")  # Процент скидки
    start_date = models.DateField()  # Дата начала действия
    end_date = models.DateField()  # Дата окончания действия
    max_uses = models.PositiveIntegerField(default=1)  # Максимальное количество использований
    used_count = models.PositiveIntegerField(default=0)  # Количество использований
    is_active = models.BooleanField(default=True)  # Активность промокода
    services = models.ManyToManyField('Service', blank=True)  # Связь с услугами

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def remaining_uses(self):
        # Вычисление оставшегося количества использований
        return self.max_uses - self.used_count


class Appointment(models.Model):
    # Модель записи на прием
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Связь с клиентом
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Связь с врачом
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Связь с услугой
    date_time = models.DateTimeField()  # Дата и время записи
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Статус записи
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name="Причина отмены")  # Причина отмены
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, blank=True, null=True)  # Связь с промокодом

    def __str__(self):
        return f"{self.client} -> {self.doctor} ({self.date_time})"


class News(models.Model):
    # Модель новости
    title = models.CharField(max_length=200, verbose_name="Заголовок")  # Заголовок новости
    content = models.TextField(verbose_name="Содержание")  # Содержание новости
    image = models.ImageField(upload_to='news/', verbose_name="Изображение", null=True, blank=True)  # Изображение новости
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")  # Дата публикации
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")  # Автор новости
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")  # Статус публикации

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']  # Сортировка по дате публикации (новые сверху)

    def __str__(self):
        return self.title