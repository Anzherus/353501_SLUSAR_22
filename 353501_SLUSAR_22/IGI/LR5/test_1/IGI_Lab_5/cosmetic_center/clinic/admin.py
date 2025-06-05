# admin.py
from django.contrib import admin
from .models import (
    DoctorSpecialization,
    Doctor,
    Service,
    Client,
    Appointment,
    Review,
    PromoCode,
    News
)

admin.site.register(DoctorSpecialization)
admin.site.register(Doctor)
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Appointment)
admin.site.register(Review)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)