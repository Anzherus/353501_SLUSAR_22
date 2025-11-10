# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Client, Doctor, Appointment, Service, News, PromoCode,
    Product, ProductCategory, CartItem, FAQ, Vacancy, 
    CompanyInfo, Banner, PrivacyPolicy
)
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone


class ClientSignUpForm(UserCreationForm):
    """
    Form for client registration
    """
    first_name = forms.CharField(max_length=100, required=True)  # Required field, max 100 characters
    last_name = forms.CharField(max_length=100, required=True)   # Required field, max 100 characters
    email = forms.EmailField(required=True)                      # Required field, email format validation
    phone = forms.CharField(max_length=20, help_text="Формат: +375 (29) XXX-XX-XX")  # Max 20 characters
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Вы должны быть старше 18 лет"
    )
    address = forms.CharField(widget=forms.Textarea)  # Text field for address
    privacy_policy_agreement = forms.BooleanField(
        required=True,
        label="Я согласен с политикой конфиденциальности",
        help_text="<a href='/privacy-policy/' target='_blank'>Политика конфиденциальности</a>"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_birth_date(self):
        """
        Client age validation
        """
        birth_date = self.cleaned_data.get('birth_date')
        age = (date.today() - birth_date).days // 365
        if age < 18:
            raise forms.ValidationError("Вы должны быть старше 18 лет!")
        return birth_date


class DoctorSignUpForm(UserCreationForm):
    """
    Form for doctor registration
    """
    first_name = forms.CharField(max_length=100, required=True)  # Required field, max 100 characters
    last_name = forms.CharField(max_length=100, required=True)   # Required field, max 100 characters
    email = forms.EmailField(required=True)                      # Required field, email format validation
    specialization = forms.CharField(max_length=100)             # Max 100 characters
    experience = forms.IntegerField(min_value=0)                 # Minimum value 0
    bio = forms.CharField(widget=forms.Textarea)                 # Text field for biography
    photo = forms.ImageField()                                   # Field for image upload

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ReviewForm(forms.Form):
    """
    Form for customer reviews
    """
    RATING_CHOICES = [
        (1, '1 - Плохо'),
        (2, '2 - Удовлетворительно'),
        (3, '3 - Хорошо'),
        (4, '4 - Очень хорошо'),
        (5, '5 - Отлично'),
    ]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES, 
        widget=forms.RadioSelect,
        label="Оценка",
        help_text="Выберите оценку от 1 до 5"
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Опишите ваши впечатления...'}),
        label="Текст отзыва",
        help_text="Поделитесь вашими впечатлениями о нашем центре"
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        required=False,
        empty_label="-- Не указывать --",
        label="Врач (если применимо)",
        help_text="Выберите врача, если отзыв касается конкретного специалиста"
    )


class PromoCodeForm(forms.ModelForm):
    """
    Form for promo code management
    """
    class Meta:
        model = PromoCode
        fields = ['name', 'code', 'discount', 'start_date', 'end_date', 'max_uses', 'is_active', 'services']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),
            'max_uses': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        """
        Promo code data validation
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        discount = cleaned_data.get('discount')

        # Date validation: check that end date is after start date
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Дата окончания должна быть позже даты начала")

        # Discount validation: check range from 1 to 100 percent
        if discount and (discount < 1 or discount > 100):
            raise forms.ValidationError("Скидка должна быть от 1 до 100 процентов")

        return cleaned_data

    def clean_code(self):
        """
        Promo code uniqueness validation
        """
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()  # Convert to uppercase
            # Check for existing promo code with same code
            if PromoCode.objects.filter(code=code).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise forms.ValidationError("Промокод с таким кодом уже существует")
        return code


class AppointmentStatusForm(forms.ModelForm):
    """
    Form for updating appointment status
    """
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
        """
        Validate appointment status and cancellation reason
        """
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        cancellation_reason = cleaned_data.get('cancellation_reason')

        # Check if cancellation reason is provided when canceling appointment
        if status == 'canceled' and not cancellation_reason:
            raise forms.ValidationError("При отмене записи необходимо указать причину")

        return cleaned_data


class AppointmentForm(forms.ModelForm):
    """
    Form for appointment booking
    """
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
        required=False,  # Optional field
        label='Комментарий'
    )

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'doctor', 'notes']

    def clean(self):
        """
        Validate appointment date and time
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        if date and time:
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(date, time)
            )
            # Check that appointment date and time are not in the past
            if appointment_datetime < timezone.now():
                raise ValidationError("Нельзя записываться на прошедшую дату и время")
        
        return cleaned_data


class NewsForm(forms.ModelForm):
    """
    Form for news management
    """
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
        """
        News title validation
        """
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError("Заголовок должен содержать минимум 5 символов")
        return title

    def clean_content(self):
        """
        News content validation
        """
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise ValidationError("Содержание новости должно содержать минимум 50 символов")
        return content


class ProductForm(forms.ModelForm):
    """
    Form for product management
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'short_description', 'price', 'category', 'image', 'stock_quantity', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductCategoryForm(forms.ModelForm):
    """
    Form for product category management
    """
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CartItemForm(forms.ModelForm):
    """
    Form for cart item management
    """
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '99'}),
        }


class FAQForm(forms.ModelForm):
    """
    Form for FAQ management
    """
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category', 'is_active', 'order']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VacancyForm(forms.ModelForm):
    """
    Form for vacancy management
    """
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'requirements', 'salary', 'location', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CompanyInfoForm(forms.ModelForm):
    """
    Form for company information management
    """
    class Meta:
        model = CompanyInfo
        fields = ['name', 'logo', 'description', 'video_url', 'video_file', 'requisites', 'history', 'certificate']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://www.youtube.com/embed/VIDEO_ID (необязательно)'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/mp4'
            }),
            'requisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'history': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'certificate': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        """
        Validate video fields
        """
        cleaned_data = super().clean()
        video_url = cleaned_data.get('video_url')
        video_file = cleaned_data.get('video_file')
        
        # Check that at least one video option is provided
        if not video_url and not video_file:
            raise forms.ValidationError("Необходимо указать либо ссылку на видео, либо загрузить видео файл")
        
        return cleaned_data


class BannerForm(forms.ModelForm):
    """
    Form for banner management
    """
    class Meta:
        model = Banner
        fields = ['title', 'image', 'link_url', 'position', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'link_url': forms.URLInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PrivacyPolicyForm(forms.ModelForm):
    """
    Form for privacy policy management
    """
    class Meta:
        model = PrivacyPolicy
        fields = ['title', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }