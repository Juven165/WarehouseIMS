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
        ("In Stock", "In Stock"),
        ("Low Stock", "Low Stock"),
        ("Out Stock", "Out Stock"),
    ]

    STOCK_IN = "Stock In"
    STOCK_OUT = "Stock Out"
    ADJUSTMENT = "Adjustment"

    TRANSACTION_CHOICES = [
        (STOCK_IN, "Stock In"),
        (STOCK_OUT, "Stock Out"),
        (ADJUSTMENT, "Adjustment"),
    ]

    ADJUSTMENT_INCREASE = "Increase"
    ADJUSTMENT_DECREASE = "Decrease"

    ADJUSTMENT_TYPE_CHOICES = [
        (ADJUSTMENT_INCREASE, "Increase"),
        (ADJUSTMENT_DECREASE, "Decrease"),
    ]

    adjustment_type = models.CharField(
        max_length=10,
        choices=ADJUSTMENT_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Only used when transaction_type is Adjustment"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_CHOICES
    )
    quantity = models.PositiveIntegerField()
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(max_length=500, blank=True)
    supplier = models.ForeignKey("Supplier", on_delete=models.SET_NULL, null=True)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} ({self.quantity})"

class Supplier(models.Model):
    SUPPLIER_NOTES = [
        ("reliable", "Reliable"),
        ("preferred", "Preferred"),
        ("late", "Late Delivery"),
        ("blacklisted", "Blacklisted"),
        ("new", "New Supplier"),
    ]

    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    notes = models.CharField(
        max_length=30,
        choices=SUPPLIER_NOTES,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.description}'