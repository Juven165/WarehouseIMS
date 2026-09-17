from django.urls import path
from . import views

urlpatterns = [
    path('supplier-dashboard/', views.SupplierDashboard.as_view(), name='supplier_dashboard'),
    path('supplier/supplier-delivery/', views.SupplierMyDeliveries.as_view(), name='supplier_deliveries'),
    path('supplier/submit-inventory/', views.submit_inventory, name='submit_inventory'),
    path('staff/view-details/<int:product_id>/', views.view_details, name='view_details'),
    path('staff/my_report/', views.my_report, name='my_report'),
    path('staff/edit-delivery/<int:pk>/', views.edit_delivery, name='edit_delivery'),
    path('delete-delivery/<int:pk>/', views.delete_delivery, name='delete_delivery'),
]