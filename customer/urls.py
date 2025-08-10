from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.customer_register, name='customer_register'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('list/', views.customer_list, name='customer_list'),
    path('<int:customer_id>/detail/', views.customer_detail_staff, name='customer_detail_staff'),
    path('staff/select-product/<int:customer_id>/', views.select_product, name='select_product'),

]