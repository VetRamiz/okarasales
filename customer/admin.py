from django.contrib import admin

# Register your models here.

from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    
    list_display = ('full_name', 'user', 'cnic', 'is_active', 'approved')
    search_fields = ('full_name', 'cnic', 'user__username')
    list_filter = ('is_active', 'approved')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = 'Full Name'