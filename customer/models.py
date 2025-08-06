from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('private', 'Private Regular'),
        ('govt', 'Government Servant'),
        ('wapda', 'Wapda Servant'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    customer_picture = models.ImageField(upload_to='customer_pictures/', blank=True, null=True, help_text="Profile picture of the customer")
    full_name = models.CharField(max_length=255)
    parentage_husband = models.CharField(max_length=255, blank=True, null=True, help_text="Husband's name if applicable")
    phone = models.CharField(max_length=20)
    cnic = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES)
    occupation = models.CharField(max_length=100, blank=True, null=True, help_text="Occupation of the customer")
    office_address = models.TextField(blank=True, null=True, help_text="Office address if applicable")
    department = models.CharField(max_length=100, blank=True, null=True, help_text="Department if applicable")
    office_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Office phone number if applicable")
    period_employed=models.CharField(max_length=100, blank=True, null=True, help_text="Period of employment if applicable")
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False, help_text="Indicates if the customer profile is approved")
    attached_file = models.FileField(upload_to='customer_files/', blank=True, null=True, help_text="Attach any relevant file")
    attached_file_2 = models.FileField(upload_to='customer_files/', blank=True, null=True, help_text="Attach any relevant file")
    attached_file_3 = models.FileField(upload_to='customer_files/', blank=True, null=True, help_text="Attach any relevant file")

    def __str__(self):
        return f"{self.full_name} ({self.get_customer_type_display()})"

