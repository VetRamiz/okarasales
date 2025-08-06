from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def post_login_redirect(request):
    if hasattr(request.user, 'staff_profile'):
        return redirect('staff_dashboard')
    elif hasattr(request.user, 'customer_profile'):
        return redirect('customer_dashboard')
    else:
        return redirect('admin:index')
    
