from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.customer_register, name='customer_register'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('list/', views.customer_list, name='customer_list'),
    
]