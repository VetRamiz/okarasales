from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.staff_register, name='staff_register'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),    

]
