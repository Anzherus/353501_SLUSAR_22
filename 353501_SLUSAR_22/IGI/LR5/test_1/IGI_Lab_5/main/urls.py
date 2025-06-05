from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Public pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('faq/', views.FAQListView.as_view(), name='faq_list'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancy_list'),
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    
    # Client pages
    path('profile/', views.ClientProfileView.as_view(), name='client_profile'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/<int:pk>/cancel/', views.AppointmentCancelView.as_view(), name='appointment_cancel'),
    path('reviews/create/<int:appointment_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    
    # Doctor pages
    path('doctor/dashboard/', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('doctor/appointments/', views.DoctorAppointmentListView.as_view(), name='doctor_appointments'),
    path('doctor/schedule/', views.DoctorScheduleView.as_view(), name='doctor_schedule'),
    
    # Admin pages
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/statistics/', views.AdminStatisticsView.as_view(), name='admin_statistics'),
    path('admin/appointments/', views.AdminAppointmentListView.as_view(), name='admin_appointments'),
    
    # API endpoints
    path('api/services/', views.ServiceAPIView.as_view(), name='api_services'),
    path('api/doctors/schedule/', views.DoctorScheduleAPIView.as_view(), name='api_doctor_schedule'),
    path('api/statistics/', views.StatisticsAPIView.as_view(), name='api_statistics'),
] 