from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Sum
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    Doctor, ServiceCategory, Service, Client, 
    Appointment, Review, Promo, CompanyInfo,
    News, FAQ, Vacancy
)
import plotly.express as px
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = News.objects.order_by('-created_at').first()
        context['featured_services'] = Service.objects.all()[:6]
        context['featured_doctors'] = Doctor.objects.all()[:4]
        context['testimonials'] = Review.objects.filter(rating__gte=4)[:6]
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_info'] = CompanyInfo.objects.first()
        return context

class NewsListView(ListView):
    model = News
    template_name = 'main/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    ordering = ['-created_at']

class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'
    context_object_name = 'news'

class ServiceListView(ListView):
    model = Service
    template_name = 'main/service_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'main/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.review_set.all()[:5]
        context['doctors'] = self.object.doctors.all()
        return context

class DoctorListView(ListView):
    model = Doctor
    template_name = 'main/doctor_list.html'
    context_object_name = 'doctors'

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'main/doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.object.services.all()
        return context

class FAQListView(ListView):
    model = FAQ
    template_name = 'main/faq_list.html'
    context_object_name = 'faqs'

class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_info'] = CompanyInfo.objects.first()
        context['doctors'] = Doctor.objects.all()
        return context

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'main/vacancy_list.html'
    context_object_name = 'vacancies'
    queryset = Vacancy.objects.filter(is_active=True)

class ReviewListView(ListView):
    model = Review
    template_name = 'main/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    ordering = ['-created_at']

class TermsView(TemplateView):
    template_name = 'main/terms.html'

class PrivacyView(TemplateView):
    template_name = 'main/privacy.html'

# Client views
class ClientProfileView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'main/client_profile.html'
    fields = ['phone_number', 'address']
    success_url = reverse_lazy('main:client_profile')

    def get_object(self, queryset=None):
        return self.request.user.client

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'main/appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user.client)

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'main/appointment_form.html'
    fields = ['service', 'doctor', 'date_time']
    success_url = reverse_lazy('main:appointment_list')

    def form_valid(self, form):
        form.instance.client = self.request.user.client
        return super().form_valid(form)

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'main/appointment_detail.html'
    context_object_name = 'appointment'

class AppointmentCancelView(LoginRequiredMixin, UpdateView):
    model = Appointment
    template_name = 'main/appointment_cancel.html'
    fields = []
    success_url = reverse_lazy('main:appointment_list')

    def form_valid(self, form):
        form.instance.status = 'CANCELLED'
        return super().form_valid(form)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'main/review_form.html'
    fields = ['rating', 'comment']
    success_url = reverse_lazy('main:appointment_list')

    def form_valid(self, form):
        appointment = get_object_or_404(Appointment, id=self.kwargs['appointment_id'])
        form.instance.client = self.request.user.client
        form.instance.service = appointment.service
        return super().form_valid(form)

# Doctor views
class DoctorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/doctor_dashboard.html'

    def test_func(self):
        return hasattr(self.request.user, 'doctor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user.doctor
        today = timezone.now()
        context['today_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            date_time__date=today.date()
        )
        context['upcoming_appointments'] = Appointment.objects.filter(
            doctor=doctor,
            date_time__gt=today
        )[:5]
        return context

class DoctorAppointmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'main/doctor_appointments.html'
    context_object_name = 'appointments'

    def test_func(self):
        return hasattr(self.request.user, 'doctor')

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user.doctor)

class DoctorScheduleView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/doctor_schedule.html'

    def test_func(self):
        return hasattr(self.request.user, 'doctor')

# Admin views
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_clients'] = Client.objects.count()
        context['total_appointments'] = Appointment.objects.count()
        context['total_revenue'] = Appointment.objects.filter(
            status='COMPLETED'
        ).aggregate(
            total=Sum('service__price')
        )['total'] or 0
        return context

class AdminStatisticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'main/admin_statistics.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Service statistics
        services_data = Service.objects.annotate(
            appointment_count=Count('appointment'),
            avg_rating=Avg('review__rating')
        ).values('name', 'appointment_count', 'avg_rating', 'price')
        
        df_services = pd.DataFrame(services_data)
        
        if not df_services.empty:
            # Service popularity chart
            fig_popularity = px.bar(
                df_services,
                x='name',
                y='appointment_count',
                title='Service Popularity'
            )
            context['service_popularity_chart'] = fig_popularity.to_html()
            
            # Service ratings chart
            fig_ratings = px.bar(
                df_services,
                x='name',
                y='avg_rating',
                title='Average Service Ratings'
            )
            context['service_ratings_chart'] = fig_ratings.to_html()
        
        # Revenue over time
        appointments = Appointment.objects.filter(
            status='COMPLETED'
        ).values('date_time', 'service__price')
        
        df_revenue = pd.DataFrame(appointments)
        
        if not df_revenue.empty:
            df_revenue['date'] = pd.to_datetime(df_revenue['date_time']).dt.date
            df_revenue = df_revenue.groupby('date')['service__price'].sum().reset_index()
            
            fig_revenue = px.line(
                df_revenue,
                x='date',
                y='service__price',
                title='Daily Revenue'
            )
            context['revenue_chart'] = fig_revenue.to_html()
        
        return context

class AdminAppointmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'main/admin_appointments.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_superuser

# API Views
class ServiceAPIView(LoginRequiredMixin, ListView):
    model = Service

    def get(self, request, *args, **kwargs):
        services = self.get_queryset()
        data = [{
            'id': service.id,
            'name': service.name,
            'price': str(service.price),
            'duration': service.duration,
            'category': service.category.name
        } for service in services]
        return JsonResponse({'services': data})

class DoctorScheduleAPIView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment

    def test_func(self):
        return hasattr(self.request.user, 'doctor')

    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.filter(
            doctor=request.user.doctor,
            date_time__gte=timezone.now()
        )
        data = [{
            'id': apt.id,
            'client': apt.client.user.get_full_name(),
            'service': apt.service.name,
            'date_time': apt.date_time.isoformat(),
            'status': apt.status
        } for apt in appointments]
        return JsonResponse({'appointments': data})

class StatisticsAPIView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        # Calculate statistics
        total_clients = Client.objects.count()
        total_appointments = Appointment.objects.count()
        total_revenue = Appointment.objects.filter(
            status='COMPLETED'
        ).aggregate(
            total=Sum('service__price')
        )['total'] or 0
        
        # Most popular services
        popular_services = Service.objects.annotate(
            count=Count('appointment')
        ).values('name', 'count').order_by('-count')[:5]
        
        # Average ratings
        avg_ratings = Service.objects.annotate(
            avg_rating=Avg('review__rating')
        ).values('name', 'avg_rating')
        
        data = {
            'total_clients': total_clients,
            'total_appointments': total_appointments,
            'total_revenue': str(total_revenue),
            'popular_services': list(popular_services),
            'service_ratings': list(avg_ratings)
        }
        
        return JsonResponse(data) 