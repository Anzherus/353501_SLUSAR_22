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
    News,
    ProductCategory,
    Product,
    Cart,
    CartItem,
    FAQ,
    Vacancy,
    CompanyInfo,
    Banner,
    PrivacyPolicy,
    Partner
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

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    list_filter = ('added_at',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('order', 'created_at')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'salary', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'requirements')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'is_active', 'order', 'created_at')
    list_filter = ('position', 'is_active')
    search_fields = ('title',)
    ordering = ('order', 'created_at')

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    readonly_fields = ('created_at',)