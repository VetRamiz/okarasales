# sales/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from django.views.decorators.cache import never_cache
from django.contrib import messages

def home(request):
    return render(request, 'sales/home.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from django.views.decorators.cache import never_cache

@login_required


@never_cache
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'sales/add_product.html', {'form': form})

def product_list(request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'sales/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })

def home(request):
    return render(request, 'sales/home.html')

# in views.py
from .forms import InstallmentSaleForm, GuarantorForm
from .models import InstallmentSale, Guarantor
from customer.models import Customer
from django.shortcuts import get_object_or_404





@login_required
def assign_product_with_guarantor(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        sale_form = InstallmentSaleForm(request.POST)
        guarantor_form = GuarantorForm(request.POST)

        if sale_form.is_valid() and guarantor_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.customer = customer
            sale.save()

            guarantor = guarantor_form.save(commit=False)
            guarantor.customer = customer
            guarantor.product = sale.product
            guarantor.save()

            messages.success(request, "Product assigned with guarantor successfully.")
            return redirect('customer_list')
    else:
        sale_form = InstallmentSaleForm()
        guarantor_form = GuarantorForm()

    # Get all products with stock info
    products = Product.objects.all()

    return render(request, 'sales/assign_with_guarantor.html', {
        'sale_form': sale_form,
        'guarantor_form': guarantor_form,
        'customer': customer,
        'products': products,
    })

