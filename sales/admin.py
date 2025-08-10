from django.contrib import admin

# Register your models here.

from .models import Product, InstallmentSale

admin.site.register(Product)

admin.site.register(InstallmentSale)