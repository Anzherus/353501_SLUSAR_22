from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date


class DoctorSpecialization(models.Model):
    """
    Doctor specialization model
    Represents different medical specializations for doctors
    """
    name = models.CharField(max_length=100)  # Specialization name, max 100 characters

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """
    Doctor model
    Represents medical professionals working at the clinic
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    specialization = models.ForeignKey(DoctorSpecialization, on_delete=models.SET_NULL, null=True)  # Link to specialization
    bio = models.TextField()  # Doctor's biography
    photo = models.ImageField(upload_to='doctors/')  # Doctor's photo
    experience = models.PositiveIntegerField()  # Years of experience (positive integers only)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialization})"


class Service(models.Model):
    """
    Service model
    Represents cosmetic services offered by the clinic
    """
    name = models.CharField(max_length=200)  # Service name, max 200 characters
    description = models.TextField()  # Service description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Service price
    duration = models.DurationField()  # Service duration
    specialization = models.ForeignKey(DoctorSpecialization, on_delete=models.SET_NULL, null=True)  # Link to specialization

    def __str__(self):
        return self.name


class Client(models.Model):
    """
    Client model
    Represents customers who use clinic services
    """
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    phone = models.CharField(max_length=20)  # Phone number, max 20 characters
    birth_date = models.DateField()  # Birth date
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', verbose_name="Пол")  # Gender with predefined choices
    address = models.TextField(blank=True, verbose_name="Адрес")  # Client address

    def __str__(self):
        return self.user.get_full_name()

    def clean(self):
        """
        Client age validation at model level
        Ensures client is at least 18 years old
        """
        super().clean()
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        if age < 18:
            raise ValidationError({'birth_date': 'Клиент должен быть старше 18 лет.'})


class Review(models.Model):
    """
    Review model
    Represents customer reviews and ratings
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Link to client
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')  # Link to doctor
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    text = models.TextField()  # Review text
    created_at = models.DateTimeField(auto_now_add=True)  # Review creation date

    def __str__(self):
        return f"Отзыв от {self.client} ({self.rating}/5) для {self.doctor}"

    @property
    def client_name(self):
        """Returns client's full name or username"""
        return self.client.user.get_full_name() or self.client.user.username


class PromoCode(models.Model):
    """
    Promo code model
    Represents discount codes for services
    """
    name = models.CharField(max_length=100)  # Promo code name, max 100 characters
    code = models.CharField(max_length=20, unique=True)  # Unique promo code
    discount = models.PositiveIntegerField(help_text="Процент скидки")  # Discount percentage
    start_date = models.DateField()  # Start date
    end_date = models.DateField()  # End date
    max_uses = models.PositiveIntegerField(default=1)  # Maximum number of uses
    used_count = models.PositiveIntegerField(default=0)  # Number of uses
    is_active = models.BooleanField(default=True)  # Promo code activity status
    services = models.ManyToManyField('Service', blank=True)  # Link to services

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def remaining_uses(self):
        """Calculate remaining number of uses"""
        return self.max_uses - self.used_count


class Appointment(models.Model):
    """
    Appointment model
    Represents client appointments with doctors
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Link to client
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Link to doctor
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Link to service
    date_time = models.DateTimeField()  # Appointment date and time
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Appointment status
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name="Причина отмены")  # Cancellation reason
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, blank=True, null=True)  # Link to promo code

    def __str__(self):
        return f"{self.client} -> {self.doctor} ({self.date_time})"


class News(models.Model):
    """
    News model
    Represents news articles and announcements
    """
    title = models.CharField(max_length=200, verbose_name="Заголовок")  # News title
    content = models.TextField(verbose_name="Содержание")  # News content
    image = models.ImageField(upload_to='news/', verbose_name="Изображение", null=True, blank=True)  # News image
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")  # Publication date
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")  # News author
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")  # Publication status

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']  # Sort by publication date (newest first)

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    """
    Product category model
    Represents categories for organizing products
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='product_categories/', null=True, blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model
    Represents cosmetic products sold by the clinic
    """
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Краткое описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField(upload_to='products/', verbose_name="Основное изображение")
    images = models.JSONField(default=list, blank=True, verbose_name="Дополнительные изображения")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Shopping cart model
    Represents user's shopping cart for products
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.total_price for item in self.cartitem_set.all())

    @property
    def total_items(self):
        """Calculate total number of items in cart"""
        return sum(item.quantity for item in self.cartitem_set.all())


class CartItem(models.Model):
    """
    Cart item model
    Represents individual items in shopping cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.product.price * self.quantity


class FAQ(models.Model):
    """
    FAQ model
    Represents frequently asked questions and answers
    """
    question = models.CharField(max_length=500, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    category = models.CharField(max_length=100, blank=True, verbose_name="Категория")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.question


class Vacancy(models.Model):
    """
    Vacancy model
    Represents job openings and positions
    """
    title = models.CharField(max_length=200, verbose_name="Название должности")
    description = models.TextField(verbose_name="Описание")
    requirements = models.TextField(verbose_name="Требования")
    salary = models.CharField(max_length=100, blank=True, verbose_name="Зарплата")
    location = models.CharField(max_length=200, verbose_name="Местоположение")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    """
    Company information model
    Represents general information about the clinic
    """
    name = models.CharField(max_length=200, verbose_name="Название компании")
    logo = models.ImageField(upload_to='company/', verbose_name="Логотип")
    description = models.TextField(verbose_name="Описание")
    video_url = models.URLField(blank=True, verbose_name="Ссылка на видео (для YouTube/Vimeo)")
    video_file = models.FileField(upload_to='company/videos/', blank=True, null=True, verbose_name="Видео файл (MP4)")
    requisites = models.TextField(verbose_name="Реквизиты")
    history = models.TextField(verbose_name="История компании")
    certificate = models.ImageField(upload_to='company/', verbose_name="Сертификат")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def __str__(self):
        return self.name


class Banner(models.Model):
    """
    Banner model
    Represents promotional banners and advertisements
    """
    title = models.CharField(max_length=200, verbose_name="Название")
    image = models.ImageField(upload_to='banners/', verbose_name="Изображение")
    link_url = models.URLField(blank=True, verbose_name="Ссылка")
    position = models.CharField(max_length=20, choices=[
        ('left', 'Левый'),
        ('right', 'Правый'),
        ('top', 'Верхний'),
        ('bottom', 'Нижний')
    ], default='left', verbose_name="Позиция")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title


class PrivacyPolicy(models.Model):
    """
    Privacy policy model
    Represents privacy policy and terms of service
    """
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"

    def __str__(self):
        return self.title


class Partner(models.Model):
    """
    Partner model
    Represents business partners and collaborators
    """
    name = models.CharField(max_length=200, verbose_name="Название партнера")
    description = models.TextField(blank=True, verbose_name="Описание")
    logo = models.ImageField(upload_to='partners/', verbose_name="Логотип")
    website_url = models.URLField(verbose_name="Ссылка на сайт")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name