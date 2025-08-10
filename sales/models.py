from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from customer.models import Customer
from django.db.models import Sum  # Add this import
  # Add this import
from django.utils import timezone
from django.core.validators import MinValueValidator
# Create your models here.


from django.db import models
from django.db.models import Sum

from django.db import models
from django.db.models import Sum

from django.db import models
from django.db.models import Sum

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('appliances', 'Appliances'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    specs = models.TextField(blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    direct_cash_price = models.DecimalField(max_digits=10, decimal_places=2)
    batch = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0, help_text="Manual stock count")
    sold = models.IntegerField(default=0, help_text="Total units sold")  # ✅ NEW field
    available = models.BooleanField(default=True)
    image_1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='products/', blank=True, null=True)
    other_info = models.TextField(blank=True, null=True)

    def update_availability(self):
        """Keeps 'available' in sync with stock."""
        self.available = self.stock - self.sold > 0
        self.save(update_fields=['available'])

    @property
    def sold_quantity(self):
        return self.installmentsale_set.aggregate(total=Sum('quantity'))['total'] or 0

    @property
    def available_stock(self):
        return self.stock - self.sold

    @property
    def status(self):
        if self.available_stock > 10:
            return 'In Stock'
        elif self.available_stock > 0:
            return f'Low Stock ({self.available_stock})'
        return 'Out of Stock'

    def __str__(self):
        return f"{self.name} (Batch: {self.batch}) - {self.status}"

class InstallmentSale(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('completed', 'Fully Paid'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    percentage_increase = models.DecimalField(max_digits=5, decimal_places=2, help_text="e.g. 10 for 10%")
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    number_of_installments = models.IntegerField()
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        is_new = self.pk is None

    # Calculate final price
        if not self.final_price:
            base_price = self.product.direct_cash_price * self.quantity
            self.final_price = base_price * (1 + self.percentage_increase / 100)

    # Calculate monthly installment
        if not self.monthly_installment and self.number_of_installments:
            self.monthly_installment = self.final_price / self.number_of_installments

    # Stock management for NEW sales only
        if is_new:
            self.product.stock -= self.quantity
            self.product.sold += self.quantity
            self.product.update_availability()
            self.product.save(update_fields=['stock', 'sold', 'available'])

        super().save(*args, **kwargs)



    
    @property
    def remaining_amount(self):
        total_paid = self.payment_set.aggregate(
            Sum('amount'))['amount__sum'] or 0
        return max(self.final_price - total_paid, 0)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity} for {self.customer}"


class Payment(models.Model):
    sale = models.ForeignKey(
        InstallmentSale, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('cash', 'Cash'),
            ('bank_transfer', 'Bank Transfer'),
            ('cheque', 'Cheque'),
            ('other', 'Other')
        ]
    )
    installment_number = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.sale.product.name} to {self.sale.customer}"

class Guarantor(models.Model):
    guarantor_name_1 = models.CharField(max_length=255, blank=True, null=True, help_text="Guarantor's name if applicable")
    guarantor_cnic_1 = models.CharField(max_length=15, blank=True, null=True, help_text="Guarantor's CNIC if applicable")
    guarantor_contact_1 = models.CharField(max_length=20, blank=True, null=True, help_text="Guarantor's contact number if applicable")
    guarantor_name_2 = models.CharField(max_length=255, blank=True, null=True, help_text="Second guarantor's name if applicable")
    guarantor_cnic_2 = models.CharField(max_length=15, blank=True, null=True, help_text="Second guarantor's CNIC if applicable")
    guarantor_contact_2 = models.CharField(max_length=20, blank=True, null=True, help_text="Second guarantor's contact number if applicable")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='guarantors')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='guarantors')

