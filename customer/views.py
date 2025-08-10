from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import CustomerUserForm, CustomerProfileForm
from sales.forms import InstallmentSaleForm, GuarantorForm
from django.contrib import messages


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
from sales.models import InstallmentSale, Product # assuming this links customer & product

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from sales.models import InstallmentSale, Payment
@login_required
def customer_dashboard(request):
    customer = Customer.objects.get(user=request.user)
    sales = InstallmentSale.objects.filter(customer=customer).select_related('product')
    
    # Prepare payment info per sale
    payment_info = {}
    for sale in sales:
        payments = Payment.objects.filter(sale=sale).order_by('payment_date')
        total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
        remaining = sale.final_price - total_paid
        remaining_installments = max(0, sale.number_of_installments - payments.count())

        payment_info[sale.id] = {
            'payments': payments,
            'total_paid': total_paid,
            'remaining': remaining,
            'remaining_installments': remaining_installments,
        }

    return render(request, 'customer/customer_dashboard.html', {
        'customer': customer,
        'sales': sales,
        'payment_info': payment_info,
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
        customers = customers.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query)
        )

    # Gather each customer's assigned products (multiple sales)
    customer_data = []
    for customer in customers:
        sales = InstallmentSale.objects.filter(customer=customer)
        if sales.exists():
            for sale in sales:
                customer_data.append({
                    'customer': customer,
                    'sale': sale,
                })
        else:
            customer_data.append({
                'customer': customer,
                'sale': None,
            })

    return render(request, 'customer/customer_list.html', {
        'customer_data': customer_data
    })


from django.shortcuts import render, get_object_or_404
from sales.models import InstallmentSale, Guarantor, Payment

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from sales.models import InstallmentSale, Guarantor, Payment

from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from sales.models import InstallmentSale, Guarantor, Payment
from django.contrib.auth.decorators import login_required

@login_required
def customer_detail_staff(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    purchases = InstallmentSale.objects.filter(customer=customer).select_related('product')
    guarantors = Guarantor.objects.filter(customer=customer)

    # Group payments by sale
    payments_by_sale = {}
    for sale in purchases:
        related_payments = Payment.objects.filter(sale=sale).order_by('payment_date')
        total_paid = related_payments.aggregate(total=Sum('amount'))['total'] or 0
        remaining = sale.final_price - total_paid
        payments_by_sale[sale.id] = {
            'payments': related_payments,
            'total_paid': total_paid,
            'remaining': remaining,
        }

    return render(request, 'customer/customer_detail_staff.html', {
        'customer': customer,
        'purchases': purchases,
        'guarantors': guarantors,
        'payments_by_sale': payments_by_sale,
    })
# customers/views.py
from django.core.paginator import Paginator
from django.db.models import Q

from django.core.paginator import Paginator
from django.db.models import Q

from django.db.models import Q, F, ExpressionWrapper, IntegerField
from django.core.paginator import Paginator

from django.db.models import Q, F
from django.core.paginator import Paginator
from django.apps import apps
@login_required
def select_product(request, customer_id):
    query = request.GET.get('q', '')

    # Annotate with a DIFFERENT name to avoid conflict with @property
    products_qs = Product.objects.annotate(
        available_stock_db=F('stock') - F('sold')
    ).filter(available_stock_db__gt=0)

    # Detect if category is FK or CharField
    category_field = Product._meta.get_field('category')
    if query:
        search_filter = Q(name__icontains=query)
        if category_field.is_relation:  # ForeignKey or ManyToOne
            rel_model = category_field.related_model
            if 'name' in [f.name for f in rel_model._meta.fields]:
                search_filter |= Q(category__name__icontains=query)
        else:
            search_filter |= Q(category__icontains=query)

        products_qs = products_qs.filter(search_filter)

    # Pagination (30 per page)
    paginator = Paginator(products_qs, 30)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'customer/select_product.html', {
        'products': products_page,
        'customer_id': customer_id,
        'query': query,
    })
