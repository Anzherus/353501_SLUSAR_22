# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import (
    Client, Doctor, DoctorSpecialization, Service, Appointment, Review, PromoCode, News,
    Product, ProductCategory, Cart, CartItem, FAQ, Vacancy, CompanyInfo, Banner, PrivacyPolicy, Partner
)
from .forms import (
    ClientSignUpForm, DoctorSignUpForm, ReviewForm, AppointmentForm, PromoCodeForm, 
    AppointmentStatusForm, NewsForm, ProductForm, ProductCategoryForm, CartItemForm,
    FAQForm, VacancyForm, CompanyInfoForm, BannerForm, PrivacyPolicyForm
)
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncMonth
import numpy as np
from datetime import date, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from .currency_api import convert_price


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


def get_available_dates():
    """
    Generate available appointment dates for the next 14 days
    Excludes weekends (Saturday and Sunday)
    """
    today = date.today()
    available_dates = []
    
    # Generate dates for the next 14 days
    for i in range(14):
        current_date = today + timedelta(days=i)
        # Skip weekends (5 - Saturday, 6 - Sunday)
        if current_date.weekday() < 5:  # 0-4 is Monday-Friday
            available_dates.append(current_date)
    
    return available_dates


def home(request):
    """
    Home page view
    Displays popular services, latest reviews, news, and available appointment dates
    """
    # Most popular services by number of appointments
    popular_services = Service.objects.annotate(num_appointments=Count('appointment')).order_by('-num_appointments')[:3]
    # Latest reviews
    latest_reviews = Review.objects.order_by('-created_at')[:4]
    # Latest published news
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]
    # Get available appointment dates
    available_dates = get_available_dates()
    # Banners are now hardcoded in HTML template
    
    # Get active partners
    partners = Partner.objects.filter(is_active=True).order_by('order', 'name')
    
    services = Service.objects.all()[:3]
    reviews = Review.objects.order_by('-created_at')[:3]
    
    # Get cart items count for authenticated users
    cart_items_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items_count = cart.total_items
        except Cart.DoesNotExist:
            cart_items_count = 0
    
    return render(request, 'clinic/home.html', {
        'services': services,
        'reviews': reviews,
        'popular_services': popular_services,
        'latest_reviews': latest_reviews,
        'latest_news': latest_news,
        'available_dates': available_dates,
        'partners': partners,
        'cart_items_count': cart_items_count,
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

    # Clients
    clients = Client.objects.all()
    total_clients = clients.count()
    today = date.today()
    ages = [today.year - c.birth_date.year - ((today.month, today.day) < (c.birth_date.month, c.birth_date.day)) for c in clients if c.birth_date]
    avg_client_age = np.mean(ages) if ages else 0
    median_client_age = np.median(ages) if ages else 0
    # Age groups
    age_groups = [0, 20, 30, 40, 50, 200]
    age_groups_labels = ["до 20", "21-30", "31-40", "41-50", "51+"]
    clients_by_age = [len([a for a in ages if age_groups[i] < a <= age_groups[i+1]]) for i in range(len(age_groups)-1)]
    # Gender
    male_clients = clients.filter(gender='M').count()
    female_clients = clients.filter(gender='F').count()
    male_clients_percentage = round(male_clients / total_clients * 100, 1) if total_clients else 0
    female_clients_percentage = round(female_clients / total_clients * 100, 1) if total_clients else 0

    # Appointments
    appointments = Appointment.objects.all()
    total_appointments = appointments.count()
    completed_appointments = appointments.filter(status='completed').count()
    active_appointments = appointments.filter(status='pending').count()
    # Revenue (from completed appointments)
    completed = appointments.filter(status='completed')
    total_revenue = sum(a.service.price for a in completed)

    # Appointments by month
    monthly = appointments.annotate(month=TruncMonth('date_time')).values('month').annotate(count=Count('id')).order_by('month')
    months = [m['month'].strftime('%b %Y') for m in monthly]
    appointments_per_month = [m['count'] for m in monthly]

    # Revenue and statistics by services
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

            # Top doctors
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
        # Check if user has associated Client object
        try:
            client = request.user.client
        except Client.DoesNotExist:
            # If user doesn't have client profile, create one
            client = Client.objects.create(
                user=request.user,
                phone_number='',
                birth_date=None
            )
        
        appointments = Appointment.objects.filter(client=client)

        # Separate appointments by status
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
        # In case of error, show page with empty lists
        return render(request, 'clinic/my_appointments.html', {
            'upcoming_appointments': [],
            'completed_appointments': [],
            'cancelled_appointments': [],
            'error': f'Ошибка при загрузке записей: {str(e)}'
        })


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
    
    # Check if user is admin
    if user.is_staff or user.is_superuser:
        # Statistics for admin
        total_clients = Client.objects.count()
        total_doctors = Doctor.objects.count()
        total_appointments = Appointment.objects.count()
        total_reviews = Review.objects.count()
        
        return render(request, 'clinic/admin_profile.html', {
            'user': user,
            'total_clients': total_clients,
            'total_doctors': total_doctors,
            'total_appointments': total_appointments,
            'total_reviews': total_reviews,
        })
    elif hasattr(user, 'client'):
        try:
            client = user.client
        except Client.DoesNotExist:
            # Create client profile if it doesn't exist
            client = Client.objects.create(
                user=user,
                phone='',
                birth_date='1990-01-01'
            )
        
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

    # Add usage percentage calculation
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
    # Get base QuerySet
    appointments = Appointment.objects.select_related('client', 'doctor', 'service')

    # Apply filters
    year = request.GET.get('year')
    month = request.GET.get('month')
    status = request.GET.get('status')

    if year:
        appointments = appointments.filter(date_time__year=year)
    if month:
        appointments = appointments.filter(date_time__month=month)
    if status:
        appointments = appointments.filter(status=status)

    # Handle POST requests (delete and status change)
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Appointment.objects.filter(id=request.POST['delete_id']).delete()
        elif 'update_id' in request.POST:
            appointment = Appointment.objects.get(id=request.POST['update_id'])
            new_status = request.POST.get('status')
            if new_status in dict(Appointment.STATUS_CHOICES):
                appointment.status = new_status
                appointment.save()

    # Sort by date (newest first)
    appointments = appointments.order_by('-date_time')

    # Get list of available years and months for filters
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
    
    # Get prices in different currencies
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
            # Collect date and time from POST
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
            # Collect date and time from POST
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
            # Add service by doctor specialization
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


def news_list(request):
    # View for displaying all news list
    news_list = News.objects.filter(is_published=True)
    paginator = Paginator(news_list, 10)  # 10 news items per page
    page = request.GET.get('page')
    news = paginator.get_page(page)
    return render(request, 'clinic/news_list.html', {'news': news})


def news_detail(request, news_id):
    # View for displaying detailed news information
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
    # Get latest published news
    latest_news = News.objects.filter(is_published=True).order_by('-created_at').first()
    
    # Get list of doctors
    doctors = Doctor.objects.all()
    
    # Get list of services
    services = Service.objects.all()
    
    context = {
        'latest_news': latest_news,
        'doctors': doctors,
        'services': services,
    }
    
    return render(request, 'clinic/index.html', context)


# Product views
def products(request):
    products_list = Product.objects.filter(is_active=True)
    categories = ProductCategory.objects.filter(is_active=True)
    search_query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', '')

    if category_id:
        products_list = products_list.filter(category_id=category_id)

    if search_query:
        products_list = products_list.filter(name__icontains=search_query)

    if sort == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort == 'price_desc':
        products_list = products_list.order_by('-price')
    elif sort == 'name_asc':
        products_list = products_list.order_by('name')
    elif sort == 'name_desc':
        products_list = products_list.order_by('-name')

    return render(request, 'clinic/products.html', {
        'products': products_list,
        'categories': categories,
        'search_query': search_query,
        'category_id': category_id,
        'sort': sort,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'clinic/product_detail.html', {'product': product})


# Cart views
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    if request.method == 'POST':
        if 'update_quantity' in request.POST:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
            try:
                cart_item = CartItem.objects.get(id=item_id, cart=cart)
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                pass
        elif 'remove_item' in request.POST:
            item_id = request.POST.get('item_id')
            try:
                CartItem.objects.get(id=item_id, cart=cart).delete()
            except CartItem.DoesNotExist:
                pass
        return redirect('cart')
    
    return render(request, 'clinic/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Check if enough stock available
        if cart_item.quantity < product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, 'Недостаточно товара на складе')
            return redirect('product_detail', pk=product.id)
    
    return redirect('cart')


@login_required
def payment(request):
    """
    Payment page view
    For this flow: on submit, clear the user's cart and redirect to cart.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    if request.method == 'POST':
        # Clear the cart and go to cart page
        cart_items.delete()
        messages.success(request, 'Заказ оформлен. Корзина очищена.')
        return redirect('cart')

    return render(request, 'clinic/payment.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


# FAQ views
def faq(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order', 'created_at')
    categories = FAQ.objects.filter(is_active=True).values_list('category', flat=True).distinct()
    return render(request, 'clinic/faq.html', {
        'faqs': faqs,
        'categories': categories,
    })


# Vacancy views
def vacancies(request):
    vacancies_list = Vacancy.objects.filter(is_active=True).order_by('-created_at')
    # Preprocess text fields into line lists to avoid per-character iteration in templates
    def _split_lines(value):
        if not value:
            return []
        if not isinstance(value, str):
            try:
                value = str(value)
            except Exception:
                return []
        lines = [line.strip('-• \t').strip() for line in value.replace('\r\n', '\n').split('\n')]
        return [line for line in lines if line]

    for vac in vacancies_list:
        # Attach computed properties for template rendering
        try:
            vac.requirements_list = _split_lines(getattr(vac, 'requirements', ''))
        except Exception:
            vac.requirements_list = []
        try:
            vac.benefits_list = _split_lines(getattr(vac, 'benefits', ''))
        except Exception:
            vac.benefits_list = []

    return render(request, 'clinic/vacancies.html', {'vacancies': vacancies_list})


# Privacy policy views
def privacy_policy(request):
    policy = PrivacyPolicy.objects.filter(is_active=True).first()
    return render(request, 'clinic/privacy_policy.html', {'policy': policy})


def demo(request):
    """Демонстрационная страница с CSS техниками"""
    return render(request, 'clinic/demo.html')


def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'clinic/about.html', {'company_info': company_info})


def forms_demo(request):
    """Render a comprehensive forms showcase page with examples and accessibility notes."""
    return render(request, 'clinic/forms.html')


# Updated review view
def all_reviews(request):
    reviews = Review.objects.select_related('client', 'doctor').all().order_by('-created_at')
    return render(request, 'clinic/all_reviews.html', {'reviews': reviews})


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                try:
                    client = request.user.client
                except Client.DoesNotExist:
                    # Если у пользователя нет профиля клиента, создаем его
                    client = Client.objects.create(
                        user=request.user,
                        phone='',
                        birth_date='1990-01-01'
                    )
                
                doctor = form.cleaned_data.get('doctor')
                Review.objects.create(
                    client=client,
                    rating=form.cleaned_data['rating'],
                    text=form.cleaned_data['text'],
                    doctor=doctor if doctor else None
                )
                messages.success(request, 'Отзыв успешно добавлен!')
                return redirect('all_reviews')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении отзыва: {str(e)}')
                return render(request, 'clinic/add_review.html', {'form': form})
    else:
        form = ReviewForm()
    return render(request, 'clinic/add_review.html', {'form': form})