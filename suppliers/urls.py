from django.urls import path
from . import views

urlpatterns = [
    path('supplier-dashboard/', views.SupplierDashboard.as_view(), name='supplier_dashboard'),
    path('supplier/supplier-delivery/', views.SupplierMyDeliveries.as_view(), name='supplier_deliveries'),
]