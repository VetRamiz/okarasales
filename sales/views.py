# sales/views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .forms import InstallmentSaleForm, GuarantorForm
from .models import InstallmentSale, Guarantor
from customer.models import Customer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Product, Payment
from .forms import PaymentForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import PaymentForm

def home(request):
    return render(request, 'sales/home.html')

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

def product_search(request):
    term = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    
    if term:
        products = products.filter(
            Q(name__icontains=term) |
            Q(batch__icontains=term) |
            Q(search_tags__icontains=term)
        )[:20]  # Limit results
        
    results = [{
        'id': p.id,
        'text': f"{p.name} (Batch: {p.batch}) - Rs.{p.direct_cash_price}",
        'price': float(p.direct_cash_price),
        'stock': p.available_stock,
        'image': p.image_1.url if p.image_1 else None
    } for p in products]
    
    return JsonResponse({'results': results})

@login_required
def assign_product_with_guarantor(request, customer_id, product_id):
    customer = get_object_or_404(Customer, id=customer_id)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        sale_form = InstallmentSaleForm(request.POST)
        guarantor_form = GuarantorForm(request.POST)

        if sale_form.is_valid() and guarantor_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.customer = customer
            sale.product = product
            sale.save()  # Stock & sold handled in save()

            guarantor = guarantor_form.save(commit=False)
            guarantor.customer = customer
            guarantor.product = product
            guarantor.save()

            messages.success(request, 'Product successfully assigned.')
            return redirect('staff_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        sale_form = InstallmentSaleForm()
        guarantor_form = GuarantorForm()

    return render(request, 'sales/assign_with_guarantor.html', {
        'sale_form': sale_form,
        'guarantor_form': guarantor_form,
        'customer': customer,
        'product': product,
    })


@login_required
def payment_history_add(request, sale_id):
    sale = get_object_or_404(InstallmentSale, id=sale_id)
    payments = sale.payments.all()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.sale = sale
            payment.save()
            messages.success(request, "Payment added successfully.")
            return redirect('payment_history_add', sale_id=sale.id)
    else:
        form = PaymentForm()

    return render(request, 'sales/payment_history.html', {
        'sale': sale,
        'payments': payments,
        'form': form
    })
