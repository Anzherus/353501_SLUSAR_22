# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Doctor, Appointment, Service, News
from datetime import date
from .models import PromoCode
from django.core.exceptions import ValidationError
from django.utils import timezone


class ClientSignUpForm(UserCreationForm):
    # Валидация полей регистрации клиента
    first_name = forms.CharField(max_length=100, required=True)  # Обязательное поле, максимум 100 символов
    last_name = forms.CharField(max_length=100, required=True)   # Обязательное поле, максимум 100 символов
    email = forms.EmailField(required=True)                      # Обязательное поле, проверка формата email
    phone = forms.CharField(max_length=20, help_text="Формат: +375 (29) XXX-XX-XX")  # Максимум 20 символов
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Вы должны быть старше 18 лет"
    )
    address = forms.CharField(widget=forms.Textarea)  # Текстовое поле для адреса

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_birth_date(self):
        # Валидация возраста клиента
        birth_date = self.cleaned_data.get('birth_date')
        age = (date.today() - birth_date).days // 365
        if age < 18:
            raise forms.ValidationError("Вы должны быть старше 18 лет!")
        return birth_date

class DoctorSignUpForm(UserCreationForm):
    # Валидация полей регистрации врача
    first_name = forms.CharField(max_length=100, required=True)  # Обязательное поле, максимум 100 символов
    last_name = forms.CharField(max_length=100, required=True)   # Обязательное поле, максимум 100 символов
    email = forms.EmailField(required=True)                      # Обязательное поле, проверка формата email
    specialization = forms.CharField(max_length=100)             # Максимум 100 символов
    experience = forms.IntegerField(min_value=0)                 # Минимальное значение 0
    bio = forms.CharField(widget=forms.Textarea)                 # Текстовое поле для биографии
    photo = forms.ImageField()                                   # Поле для загрузки изображения

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ReviewForm(forms.Form):
    # Валидация полей отзыва
    RATING_CHOICES = [
        (1, '1 - Плохо'),
        (2, '2 - Удовлетворительно'),
        (3, '3 - Хорошо'),
        (4, '4 - Очень хорошо'),
        (5, '5 - Отлично'),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)  # Выбор из предопределенных значений
    text = forms.CharField(widget=forms.Textarea)  # Текстовое поле для отзыва



class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['name', 'code', 'discount', 'start_date', 'end_date', 'max_uses', 'is_active', 'services']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),  # Валидация диапазона скидки
            'max_uses': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),  # Минимальное значение 1
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        # Валидация данных промокода
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        discount = cleaned_data.get('discount')

        # Валидация дат: проверка, что дата окончания позже даты начала
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Дата окончания должна быть позже даты начала")

        # Валидация скидки: проверка диапазона от 1 до 100 процентов
        if discount and (discount < 1 or discount > 100):
            raise forms.ValidationError("Скидка должна быть от 1 до 100 процентов")

        return cleaned_data

    def clean_code(self):
        # Валидация уникальности кода промокода
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()  # Преобразование в верхний регистр
            # Проверка на существование промокода с таким же кодом
            if PromoCode.objects.filter(code=code).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise forms.ValidationError("Промокод с таким кодом уже существует")
        return code

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'cancellation_reason']


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'cancellation_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'cancellation_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Укажите причину отмены (если требуется)'
            }),
        }

    def clean(self):
        # Валидация статуса записи и причины отмены
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        cancellation_reason = cleaned_data.get('cancellation_reason')

        # Проверка наличия причины при отмене записи
        if status == 'canceled' and not cancellation_reason:
            raise forms.ValidationError("При отмене записи необходимо указать причину")

        return cleaned_data




class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    # Валидация полей записи на прием
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата'
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Время'
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        label='Врач'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,  # Необязательное поле
        label='Комментарий'
    )

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'doctor', 'notes']

    def clean(self):
        # Валидация даты и времени записи
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        if date and time:
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(date, time)
            )
            # Проверка, что дата и время записи не в прошлом
            if appointment_datetime < timezone.now():
                raise ValidationError("Нельзя записываться на прошедшую дату и время")
        
        return cleaned_data

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_title(self):
        # Валидация заголовка новости
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError("Заголовок должен содержать минимум 5 символов")
        return title

    def clean_content(self):
        # Валидация содержания новости
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise ValidationError("Содержание новости должно содержать минимум 50 символов")
        return content


