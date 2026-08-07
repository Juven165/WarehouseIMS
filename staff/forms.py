from django import forms
from .models import StockTransaction

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['product', 'quantity', 'supplier', 'reference_no', 'notes']