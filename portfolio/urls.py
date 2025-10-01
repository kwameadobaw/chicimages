from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:category_slug>/', views.portfolio, name='portfolio_category'),
    path('booking/', views.booking, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('personalities/', views.personalities, name='personalities'),
    path('personalities/<slug:slug>/', views.personality_detail, name='personality_detail'),
]