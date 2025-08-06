from django import forms
from django.contrib.auth.models import User
from .models import Customer

class CustomerUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer #from models.py customer application
        exclude = ['user', 'approved', 'is_active', 'date_joined']
