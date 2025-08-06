from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from customer.models import Customer
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    specs = models.TextField(blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    direct_cash_price = models.DecimalField(max_digits=10, decimal_places=2)
    batch=models.CharField(max_length=100, blank=True, null=True, help_text="Batch number or identifier")
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0, help_text="Number of items in stock")
    sold = models.IntegerField(default=0, help_text="Number of items sold")
    available = models.BooleanField(default=True, help_text="Is the product available for sale?")
    image_1 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Product image")
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Additional product image")
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Another product image")
    image_4 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Another product image")
    other_info = models.TextField(blank=True, null=True, help_text="Any other relevant information about the product")

    def __str__(self):
        available = self.stock - self.sold
        return f"{self.name} (Batch: {self.batch}, Available: {available})"

class InstallmentSale(models.Model):
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

    def __str__(self):
        return f"{self.product.name} to {self.customer.username}"
    
    def save(self, *args, **kwargs):
    # Final price calculation
        if not self.final_price:
             self.final_price = self.product.direct_cash_price * (1 + self.percentage_increase / 100)
        if not self.monthly_installment and self.final_price and self.number_of_installments:
             self.monthly_installment = self.final_price / self.number_of_installments

    # Stock update
        if not self.pk:  # Only decrease stock on first save
            self.product.stock -= self.quantity
            self.product.sold += self.quantity
            self.product.available = self.product.stock > 0
            self.product.save()

        super().save(*args, **kwargs)


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('other', 'Other')
    ])
    installment_number = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.installment_sale.product.name} to {self.installment_sale.customer.username}"
    
class Guarantor(models.Model):
    guarantor_name_1 = models.CharField(max_length=255, blank=True, null=True, help_text="Guarantor's name if applicable")
    guarantor_cnic_1 = models.CharField(max_length=15, blank=True, null=True, help_text="Guarantor's CNIC if applicable")
    guarantor_contact_1 = models.CharField(max_length=20, blank=True, null=True, help_text="Guarantor's contact number if applicable")
    guarantor_name_2 = models.CharField(max_length=255, blank=True, null=True, help_text="Second guarantor's name if applicable")
    guarantor_cnic_2 = models.CharField(max_length=15, blank=True, null=True, help_text="Second guarantor's CNIC if applicable")
    guarantor_contact_2 = models.CharField(max_length=20, blank=True, null=True, help_text="Second guarantor's contact number if applicable")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='guarantors')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='guarantors')

