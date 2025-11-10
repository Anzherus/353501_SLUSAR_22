from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('forms/', views.forms_demo, name='forms_demo'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>/', views.service_detail, name='service-detail'),
    path('services/<int:pk>/book/', views.book_appointment, name='book-appointment'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor-detail'),
    path('doctors/<int:pk>/book/', views.book_doctor, name='book-doctor'),
    path('contacts/', views.contacts, name='contacts'),
    path('promo-codes/', views.promo_codes, name='promo_codes'),
    path('promo-codes/manage/', views.manage_promos, name='manage_promo_codes'),
    path('promo-codes/add/', views.add_promo_code, name='add_promo_code'),
    path('promo-codes/<int:pk>/delete/', views.delete_promo_code, name='delete_promo_code'),
    path('statistics/', views.statistics, name='statistics'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('add-review/', views.add_review, name='add_review'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html'
        ),
        name='password_change'
    ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path('manage/appointments/', views.manage_appointments, name='manage_appointments'),
    path('manage/appointments/update/<int:pk>/', views.update_appointment, name='update_appointment'),
    path('manage/promos/', views.manage_promos, name='manage_promos'),
    path('manage/promos/edit/<int:pk>/', views.edit_promo, name='edit_promo'),
    path('reviews/', views.all_reviews, name='all_reviews'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<int:news_id>/edit/', views.news_edit, name='news_edit'),
    path('news/<int:news_id>/delete/', views.news_delete, name='news_delete'),
    # Новые URL-ы для товаров и корзины
    path('products/', views.products, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('payment/', views.payment, name='payment'),
    # Новые URL-ы для FAQ, вакансий и политики конфиденциальности
    path('faq/', views.faq, name='faq'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('demo/', views.demo, name='demo'),
]