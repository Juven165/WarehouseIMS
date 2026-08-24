from django.urls import path
from . import views

urlpatterns = [
    path('supplier-dashboard/', views.SupplierDashboard.as_view(), name='supplier_dashboard'),
]