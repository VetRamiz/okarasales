from django.shortcuts import render
from .forms import StaffUserForm, StaffProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.
def staff_register(request):
    if request.method == 'POST':
        user_form = StaffUserForm(request.POST)
        profile_form = StaffProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            staff = profile_form.save(commit=False)
            staff.user = user
            staff.save()
            login(request, user)
            return redirect('staff_dashboard')  # you'll define this
    else:
        user_form = StaffUserForm()
        profile_form = StaffProfileForm()
    return render(request, 'staff/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

from django.contrib.auth.decorators import login_required

@login_required
def staff_dashboard(request):
    return render(request, 'staff/dashboard.html')
