from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    sku = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    unit = models.CharField(max_length=200, default='pcs')
    current_stock = models.PositiveIntegerField(default=0)
    low_stock = models.PositiveIntegerField(default=10)
    supplier = models.ForeignKey("Supplier", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sku} {self.name}'

class StockTransaction(models.Model):
    STAFF_CHOICES = [
        'In Stock', 'In Stock',
        'Low Stock', 'Low Stock',
        'Out Stock', 'Out Stock',
    ]

    STOCK_IN = "Stock In"
    STOCK_OUT = "Stock Out"
    ADJUSTMENT = "Adjustment"

    TRANSACTION_CHOICES = [
        (STOCK_IN, "Stock In"),
        (STOCK_OUT, "Stock Out"),
        (ADJUSTMENT, "Adjustment"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_CHOICES
    )
    quantity = models.PositiveIntegerField()
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(max_length=500, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} ({self.quantity})"

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} {self.contact_person} {self.phone} {self.email}'

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.description}'