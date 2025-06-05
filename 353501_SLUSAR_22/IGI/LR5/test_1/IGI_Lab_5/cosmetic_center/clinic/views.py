# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Client, Doctor, DoctorSpecialization, Service, Appointment, Review, PromoCode, News
from .forms import ClientSignUpForm, DoctorSignUpForm, ReviewForm, AppointmentForm, PromoCodeForm, AppointmentStatusForm, NewsForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PromoCode, Appointment
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncMonth
import numpy as np
from datetime import date, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
import calendar
from .currency_api import convert_price


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


def get_available_dates():
    today = date.today()
    available_dates = []
    
    # Генерируем даты на ближайшие 14 дней
    for i in range(14):
        current_date = today + timedelta(days=i)
        # Пропускаем выходные (5 - суббота, 6 - воскресенье)
        if current_date.weekday() < 5:  # 0-4 это понедельник-пятница
            available_dates.append(current_date)
    
    return available_dates


def home(request):
    # Самые популярные услуги по количеству записей
    popular_services = Service.objects.annotate(num_appointments=Count('appointment')).order_by('-num_appointments')[:3]
    # Последние отзывы
    latest_reviews = Review.objects.order_by('-created_at')[:4]
    # Последняя опубликованная новость
    latest_news = News.objects.filter(is_published=True).order_by('-created_at').first()
    # Получаем доступные даты для записи
    available_dates = get_available_dates()
    
    services = Service.objects.all()[:3]
    reviews = Review.objects.order_by('-created_at')[:3]
    
    return render(request, 'clinic/home.html', {
        'services': services,
        'reviews': reviews,
        'popular_services': popular_services,
        'latest_reviews': latest_reviews,
        'latest_news': latest_news,
        'available_dates': available_dates,
    })


def about(request):
    return render(request, 'clinic/about.html')


def services(request):
    services_list = Service.objects.all()
    specializations = DoctorSpecialization.objects.all()
    search_query = request.GET.get('search', '').strip()
    sort = request.GET.get('sort', '')
    category = request.GET.get('category', '')

    if category:
        services_list = services_list.filter(specialization_id=category)

    if search_query:
        services_list = services_list.filter(name__icontains=search_query)

    if sort == 'price_asc':
        services_list = services_list.order_by('price')
    elif sort == 'price_desc':
        services_list = services_list.order_by('-price')
    elif sort == 'name_asc':
        services_list = services_list.order_by('name')
    elif sort == 'name_desc':
        services_list = services_list.order_by('-name')

    return render(request, 'clinic/services.html', {
        'services': services_list,
        'specializations': specializations,
        'search_query': search_query,
        'sort': sort,
        'category': category,
    })


def doctors(request):
    doctors_list = Doctor.objects.select_related('specialization').all()
    return render(request, 'clinic/doctors.html', {
        'doctors': doctors_list
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'clinic/doctor_detail.html', {
        'doctor': doctor
    })


def contacts(request):
    return render(request, 'clinic/contacts.html')


def promo_codes(request):
    return render(request, 'clinic/promo_codes.html')


def statistics(request):
    from django.db.models import Count, Avg, Sum
    from django.db.models.functions import TruncMonth
    import numpy as np
    from datetime import date

    # Клиенты
    clients = Client.objects.all()
    total_clients = clients.count()
    today = date.today()
    ages = [today.year - c.birth_date.year - ((today.month, today.day) < (c.birth_date.month, c.birth_date.day)) for c in clients if c.birth_date]
    avg_client_age = np.mean(ages) if ages else 0
    median_client_age = np.median(ages) if ages else 0
    # Группы по возрасту
    age_groups = [0, 20, 30, 40, 50, 200]
    age_groups_labels = ["до 20", "21-30", "31-40", "41-50", "51+"]
    clients_by_age = [len([a for a in ages if age_groups[i] < a <= age_groups[i+1]]) for i in range(len(age_groups)-1)]
    # Пол
    male_clients = clients.filter(gender='M').count()
    female_clients = clients.filter(gender='F').count()
    male_clients_percentage = round(male_clients / total_clients * 100, 1) if total_clients else 0
    female_clients_percentage = round(female_clients / total_clients * 100, 1) if total_clients else 0

    # Записи
    appointments = Appointment.objects.all()
    total_appointments = appointments.count()
    completed_appointments = appointments.filter(status='completed').count()
    active_appointments = appointments.filter(status='pending').count()
    # Доход (по завершённым)
    completed = appointments.filter(status='completed')
    total_revenue = sum(a.service.price for a in completed)

    # Записи по месяцам
    monthly = appointments.annotate(month=TruncMonth('date_time')).values('month').annotate(count=Count('id')).order_by('month')
    months = [m['month'].strftime('%b %Y') for m in monthly]
    appointments_per_month = [m['count'] for m in monthly]

    # Доход и статистика по услугам
    services = Service.objects.all()
    services_names = []
    services_appointments = []
    services_revenue = []
    for service in services:
        completed_count = Appointment.objects.filter(service=service, status='completed').count()
        revenue = completed_count * float(service.price)
        services_names.append(service.name)
        services_appointments.append(completed_count)
        services_revenue.append(revenue)
    total_revenue = sum(services_revenue)
    top_services = sorted(
        [
            {
                'name': s.name,
                'appointment_count': Appointment.objects.filter(service=s, status='completed').count(),
                'total_revenue': Appointment.objects.filter(service=s, status='completed').count() * float(s.price),
            }
            for s in services
        ],
        key=lambda x: x['appointment_count'],
        reverse=True
    )[:5]

    # Топ-врачи
    doctors = Doctor.objects.annotate(
        appointment_count=Count('appointment'),
        total_revenue=Sum('appointment__service__price', filter=Q(appointment__status='completed')),
        avg_rating=Avg('reviews__rating')
    ).order_by('-appointment_count')[:5]
    doctors_names = [d.user.get_full_name() for d in doctors]
    doctors_appointments = [d.appointment_count for d in doctors]
    doctors_ratings = [d.avg_rating or 0 for d in doctors]
    top_doctors = doctors

    stats = {
        'total_clients': total_clients,
        'avg_client_age': avg_client_age,
        'median_client_age': median_client_age,
        'clients_by_age': clients_by_age,
        'age_groups_labels': age_groups_labels,
        'male_clients_percentage': male_clients_percentage,
        'female_clients_percentage': female_clients_percentage,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'active_appointments': active_appointments,
        'total_revenue': total_revenue,
        'months': months,
        'appointments_per_month': appointments_per_month,
        'services_names': services_names,
        'services_appointments': services_appointments,
        'services_revenue': services_revenue,
        'top_services': top_services,
        'doctors_names': doctors_names,
        'doctors_appointments': doctors_appointments,
        'doctors_ratings': doctors_ratings,
        'top_doctors': top_doctors,
    }
    return render(request, 'clinic/statistics.html', {'stats': stats})


@login_required
def my_appointments(request):
    try:
        if hasattr(request.user, 'doctor'):
            appointments = Appointment.objects.filter(doctor=request.user.doctor)
        elif hasattr(request.user, 'client'):
            appointments = Appointment.objects.filter(client=request.user.client)
        else:
            return redirect('home')  # Если пользователь не клиент и не врач, перенаправляем на главную

        # Разделяем записи по статусам
        upcoming_appointments = appointments.filter(
            status='pending',
            date_time__gte=timezone.now()
        ).order_by('date_time')

        completed_appointments = appointments.filter(
            status='completed'
        ).order_by('-date_time')

        cancelled_appointments = appointments.filter(
            status='cancelled'
        ).order_by('-date_time')

        return render(request, 'clinic/my_appointments.html', {
            'upcoming_appointments': upcoming_appointments,
            'completed_appointments': completed_appointments,
            'cancelled_appointments': cancelled_appointments
        })
    except Exception as e:
        # В случае ошибки перенаправляем на главную страницу
        return redirect('home')


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            client = get_object_or_404(Client, user=request.user)
            Review.objects.create(
                client=client,
                rating=form.cleaned_data['rating'],
                text=form.cleaned_data['text']
            )
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'clinic/add_review.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ClientSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if hasattr(user, 'client'):
        client = user.client
        appointments = Appointment.objects.filter(client=client).select_related('service', 'doctor').order_by('-date_time')
        return render(request, 'clinic/client_profile.html', {
            'user': user,
            'client': client,
            'appointments': appointments,
        })
    elif hasattr(user, 'doctor'):
        doctor = user.doctor
        appointments = Appointment.objects.filter(doctor=doctor).select_related('service', 'client').order_by('-date_time')
        reviews = Review.objects.filter(doctor=doctor).order_by('-created_at')
        return render(request, 'clinic/doctor_profile.html', {
            'user': user,
            'doctor': doctor,
            'appointments': appointments,
            'reviews': reviews,
        })
    else:
        return render(request, 'clinic/profile.html', {'user': user})


def client_signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            Client.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                birth_date=form.cleaned_data['birth_date'],
                address=form.cleaned_data['address']
            )

            login(request, user)
            return redirect('home')
    else:
        form = ClientSignUpForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'user_type': 'client'
    })


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            Doctor.objects.create(
                user=user,
                specialization=form.cleaned_data['specialization'],
                experience=form.cleaned_data['experience'],
                bio=form.cleaned_data['bio'],
                photo=form.cleaned_data['photo']
            )

            login(request, user)
            return redirect('home')
    else:
        form = DoctorSignUpForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'user_type': 'doctor'
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_promos(request):
    promos = PromoCode.objects.all().order_by('-is_active', '-end_date')

    # Добавляем вычисление процента использования
    for promo in promos:
        if promo.max_uses:
            promo.usage_percent = int((promo.used_count / promo.max_uses) * 100)
        else:
            promo.usage_percent = 0

    if request.method == 'POST':
        if 'delete_promo' in request.POST:
            promo_id = request.POST.get('delete_promo')
            try:
                promo = PromoCode.objects.get(id=promo_id)
                promo.delete()
                messages.success(request, 'Промокод успешно удален')
            except PromoCode.DoesNotExist:
                messages.error(request, 'Промокод не найден')
            return redirect('manage_promos')
        else:
            form = PromoCodeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Промокод успешно создан')
                return redirect('manage_promos')
    else:
        form = PromoCodeForm()

    return render(request, 'clinic/manage_promos.html', {
        'promos': promos,
        'form': form
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_promo(request, pk):
    promo = get_object_or_404(PromoCode, pk=pk)
    if request.method == 'POST':
        form = PromoCodeForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            return redirect('manage_promos')
    else:
        form = PromoCodeForm(instance=promo)

    return render(request, 'clinic/edit_promo.html', {
        'form': form,
        'promo': promo
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_promo_code(request, pk):
    promo_code = get_object_or_404(PromoCode, pk=pk)
    if request.method == 'POST':
        promo_code.delete()
        return redirect('manage_promo_codes')
    return render(request, 'clinic/delete_promo_code.html', {
        'promo_code': promo_code
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_promo_code(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_promos')
    else:
        form = PromoCodeForm()
    
    return render(request, 'clinic/add_promo_code.html', {
        'form': form
    })


@staff_member_required
def manage_appointments(request):
    # Получаем базовый QuerySet
    appointments = Appointment.objects.select_related('client', 'doctor', 'service')

    # Применяем фильтры
    year = request.GET.get('year')
    month = request.GET.get('month')
    status = request.GET.get('status')

    if year:
        appointments = appointments.filter(date_time__year=year)
    if month:
        appointments = appointments.filter(date_time__month=month)
    if status:
        appointments = appointments.filter(status=status)

    # Обработка POST-запросов (удаление и изменение статуса)
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Appointment.objects.filter(id=request.POST['delete_id']).delete()
        elif 'update_id' in request.POST:
            appointment = Appointment.objects.get(id=request.POST['update_id'])
            new_status = request.POST.get('status')
            if new_status in dict(Appointment.STATUS_CHOICES):
                appointment.status = new_status
                appointment.save()

    # Сортируем по дате (новые сверху)
    appointments = appointments.order_by('-date_time')

    # Получаем список доступных годов и месяцев для фильтров
    years = Appointment.objects.dates('date_time', 'year')
    months = Appointment.objects.dates('date_time', 'month')

    context = {
        'appointments': appointments,
        'status_choices': Appointment.STATUS_CHOICES,
        'years': years,
        'months': months,
        'current_year': year,
        'current_month': month,
        'current_status': status,
    }
    return render(request, 'clinic/manage_appointments.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('manage_appointments')
    else:
        form = AppointmentStatusForm(instance=appointment)

    return render(request, 'clinic/update_appointment.html', {
        'form': form,
        'appointment': appointment
    })


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    # Получаем цены в разных валютах
    currencies = {
        'USD': convert_price(service.price, 'USD'),
        'EUR': convert_price(service.price, 'EUR'),
        'GBP': convert_price(service.price, 'GBP'),
        'JPY': convert_price(service.price, 'JPY'),
        'CNY': convert_price(service.price, 'CNY'),
    }
    
    return render(request, 'clinic/service_detail.html', {
        'service': service,
        'currencies': currencies,
    })


@login_required
def book_appointment(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user.client
            appointment.service = service
            appointment.status = 'pending'
            # Собираем дату и время из POST
            date = request.POST.get('date')
            time = request.POST.get('time')
            if date and time:
                from datetime import datetime
                appointment.date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            else:
                form.add_error(None, "Пожалуйста, выберите дату и время приёма.")
                return render(request, 'clinic/book_appointment.html', {
                    'form': form,
                    'service': service
                })
            appointment.save()
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    
    return render(request, 'clinic/book_appointment.html', {
        'form': form,
        'service': service
    })


@login_required
def book_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user.client
            appointment.doctor = doctor
            appointment.status = 'pending'
            # Собираем дату и время из POST
            date = request.POST.get('date')
            time = request.POST.get('time')
            if date and time:
                from datetime import datetime
                appointment.date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            else:
                form.add_error(None, "Пожалуйста, выберите дату и время приёма.")
                return render(request, 'clinic/book_doctor.html', {
                    'form': form,
                    'doctor': doctor
                })
            # Добавляем услугу по специализации врача
            service = Service.objects.filter(specialization=doctor.specialization).first()
            if not service:
                form.add_error(None, "У выбранного врача нет доступных услуг.")
                return render(request, 'clinic/book_doctor.html', {
                    'form': form,
                    'doctor': doctor
                })
            appointment.service = service
            appointment.save()
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'clinic/book_doctor.html', {
        'form': form,
        'doctor': doctor
    })


def all_reviews(request):
    from .models import Review
    reviews = Review.objects.select_related('client', 'doctor').all().order_by('-id')
    return render(request, 'clinic/all_reviews.html', {'reviews': reviews})


def news_list(request):
    # Представление для отображения списка всех новостей
    news_list = News.objects.filter(is_published=True)
    paginator = Paginator(news_list, 10)  # По 10 новостей на странице
    page = request.GET.get('page')
    news = paginator.get_page(page)
    return render(request, 'clinic/news_list.html', {'news': news})


def news_detail(request, news_id):
    # Представление для отображения детальной информации о новости
    news = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'clinic/news_detail.html', {'news': news})


@login_required
@user_passes_test(lambda u: u.is_staff)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость успешно создана')
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm()
    
    return render(request, 'clinic/news_form.html', {
        'form': form,
        'action': 'Создание'
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def news_edit(request, news_id):
    news = get_object_or_404(News, id=news_id)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена')
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'clinic/news_form.html', {
        'form': form,
        'news': news,
        'action': 'Редактирование'
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def news_delete(request, news_id):
    news = get_object_or_404(News, id=news_id)
    
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость успешно удалена')
        return redirect('news_list')
    
    return render(request, 'clinic/news_confirm_delete.html', {
        'news': news
    })


def index(request):
    # Получаем последнюю опубликованную новость
    latest_news = News.objects.filter(is_published=True).order_by('-created_at').first()
    
    # Получаем список врачей
    doctors = Doctor.objects.all()
    
    # Получаем список услуг
    services = Service.objects.all()
    
    context = {
        'latest_news': latest_news,
        'doctors': doctors,
        'services': services,
    }
    
    return render(request, 'clinic/index.html', context)