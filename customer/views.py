from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import CustomerUserForm, CustomerProfileForm

def customer_register(request):
    if request.method == 'POST':
        user_form = CustomerUserForm(request.POST)
        profile_form = CustomerProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            customer = profile_form.save(commit=False)
            customer.user = user
            customer.save()
            login(request, user)
            return redirect('customer_dashboard')  # you'll define this
    else:
        user_form = CustomerUserForm()
        profile_form = CustomerProfileForm()
    return render(request, 'customer/customer_register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sales.models import InstallmentSale  # assuming this links customer & product

@login_required
def customer_dashboard(request):
    customer = request.user.customer_profile  # assuming OneToOneField from User to Customer
    sales = InstallmentSale.objects.filter(customer=customer).select_related('product')

    return render(request, 'customer/customer_dashboard.html', {
        'sales': sales
    })
from django.shortcuts import render
from customer.models import Customer
from sales.models import InstallmentSale
from django.db.models import Q

@login_required
def customer_list(request):
    query = request.GET.get('q')
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(Q(user__username__icontains=query) | Q(user__email__icontains=query))

    # Get assigned product for each customer (if any)
    customer_data = []
    for customer in customers:
        sale = InstallmentSale.objects.filter(customer=customer).first()
        customer_data.append({
            'customer': customer,
            'assigned_product': sale.product.name if sale else None,
        })

    return render(request, 'customer/customer_list.html', {'customer_data': customer_data})
