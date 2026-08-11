from django import forms
from .models import StockTransaction

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['product', 'quantity', 'supplier', 'reference_no', 'notes']

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['product', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select',
                'id': 'product-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Reason for stock out (e.g. Order #123, Damaged, etc.)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This is important part → custom label in dropdown
        self.fields['product'].label_from_instance = lambda obj: (
            f"{obj.name} (SKU: {obj.sku}) — Stock: {obj.current_stock}"
        )

class AdjustmentForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['product', 'adjustment_type', 'quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select'
            }),
            'adjustment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Reason for adjustment (required)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label_from_instance = lambda obj: (
            f"{obj.name} (SKU: {obj.sku}) — Stock: {obj.current_stock}"
        )
        self.fields['notes'].required = True  # Important for adjustments