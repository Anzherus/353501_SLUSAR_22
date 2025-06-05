from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from datetime import date
from django.core.exceptions import ValidationError

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Phone number must be in format: +375 (29) XXX-XX-XX'
            )
        ]
    )
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def clean(self):
        super().clean()
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        if age < 18:
            raise ValidationError({'birth_date': 'Врач должен быть старше 18 лет.'})

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField()
    doctors = models.ManyToManyField(Doctor, related_name='services')

    def __str__(self):
        return f"{self.name} - {self.price}$"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=19,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
                message='Phone number must be in format: +375 (29) XXX-XX-XX'
            )
        ]
    )
    birth_date = models.DateField()
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def clean(self):
        super().clean()
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        if age < 18:
            raise ValidationError({'birth_date': 'Клиент должен быть старше 18 лет.'})

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.service} with Dr. {self.doctor}"

class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1)], choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.rating}★"

class Promo(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    services = models.ManyToManyField(Service)
    description = models.TextField()

    def __str__(self):
        return f"{self.code} - {self.discount_percent}% off"

class CompanyInfo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    history = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=19)
    email = models.EmailField()
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question

class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title 