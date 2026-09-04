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


class SubmitInventoryForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['product', 'new_product_name', 'quantity', 'reference_no', 'notes']

        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select',
            }),
            'new_product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type new product name here (if not in list)'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'reference_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Batch / Lot Number',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any additional notes...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = False
        self.fields['product'].empty_label = "-- Select Existing Product --"
        self.fields['product'].label_from_instance = lambda obj: f"{obj.sku} - {obj.name}"
        self.fields['new_product_name'].required = False

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        new_product_name = cleaned_data.get('new_product_name')

        if not product and not new_product_name:
            raise forms.ValidationError("Please select a product or type a new product name.")

        if product and new_product_name:
            raise forms.ValidationError("Please choose only one: existing product OR new product name.")

        return cleaned_data