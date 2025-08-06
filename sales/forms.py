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

class InstallmentSaleForm(forms.ModelForm):
    class Meta:
        model = InstallmentSale
        fields = ['product', 'customer', 'quantity', 'percentage_increase', 'duration_months', 'number_of_installments', 'end_date']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} (Batch: {obj.batch})"
        
class GuarantorForm(forms.ModelForm):
    class Meta:
        model = Guarantor
        fields = ['guarantor_name_1', 'guarantor_cnic_1', 'guarantor_contact_1',
                  'guarantor_name_2', 'guarantor_cnic_2', 'guarantor_contact_2']
