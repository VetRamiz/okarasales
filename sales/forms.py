from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'specs', 'purchase_price', 'direct_cash_price', 'batch', 'stock', 'image_1', 'image_2', 'image_3', 'image_4', 'other_info']
         
        unique_together = ('name', 'batch')

        widgets = {
            'specs': forms.Textarea(attrs={'rows': 3}),
        }
# in forms.py
from django import forms
from .models import InstallmentSale, Guarantor

from django import forms
from .models import InstallmentSale

from django import forms
from django.db.models import Q
from .models import InstallmentSale, Product

class InstallmentSaleForm(forms.ModelForm):
    class Meta:
        model = InstallmentSale
        fields = [
            'quantity', 'percentage_increase',
            'final_price', 'duration_months', 'number_of_installments', 'end_date'
        ]


        
class GuarantorForm(forms.ModelForm):
    class Meta:
        model = Guarantor
        fields = ['guarantor_name_1', 'guarantor_cnic_1', 'guarantor_contact_1',
                  'guarantor_name_2', 'guarantor_cnic_2', 'guarantor_contact_2']
        

from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['installment_number', 'amount', 'payment_method', 'payment_date']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

