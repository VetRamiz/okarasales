from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Staff(models.Model):
    ROLE_CHOICES = [
        ('shopkeeper', 'Shopkeeper'),
        ('sales_agent', 'Sales Agent'),
        ('manager', 'Manager'),
        ('accountant', 'Accountant'),
        ('admin', 'Administrator'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    full_name = models.CharField(max_length=255)
    father_husband_name = models.CharField(max_length=255, blank=True, null=True, help_text="Father's or Husband's name if applicable")
    address = models.TextField(blank=True, null=True, help_text="Address of the staff member")
    cnic = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    staff_picture = models.ImageField(upload_to='staff_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"
