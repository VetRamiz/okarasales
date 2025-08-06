from django.urls import path
from .views import add_product, product_list, home , assign_product_with_guarantor

urlpatterns = [
    path('products/add/', add_product, name='add_product'),
    path('products/', product_list, name='product_list'),
    path('', home, name='home'), 
    path('assign-product/<int:customer_id>/', assign_product_with_guarantor, name='assign_product'),

    #path('payment-details/<int:customer_id>/', views.payment_details, name='payment_details'),

]
