from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('supplier', 'Supplier'),
        ('staff', 'Warehouse Staff'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'
    )

    is_verified = models.BooleanField(default=False)

    def is_supplier(self):
        return self.role == 'supplier'

    def is_staff_user(self):
        return self.role == 'staff'

    def is_admin_user(self):
        return self.role == 'admin'

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    company = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} Profile"