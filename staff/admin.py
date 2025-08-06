from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role', 'is_active', 'approved')
    search_fields = ('full_name', 'cnic', 'user__username')
