from django.contrib import admin
from .models import (
    Doctor, ServiceCategory, Service, Client, 
    Appointment, Review, Promo, CompanyInfo,
    News, FAQ, Vacancy
)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone_number', 'age')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization')
    list_filter = ('specialization',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    filter_horizontal = ('doctors',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'age')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'doctor', 'date_time', 'status')
    search_fields = ('client__user__username', 'service__name', 'doctor__user__username')
    list_filter = ('status', 'date_time')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'rating', 'created_at')
    search_fields = ('client__user__username', 'service__name')
    list_filter = ('rating', 'created_at')

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_until', 'is_active')
    search_fields = ('code',)
    list_filter = ('is_active', 'valid_from', 'valid_until')
    filter_horizontal = ('services',)

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary_range', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'created_at') 