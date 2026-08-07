from django.urls import path
from . import views

urlpatterns = [
    path('staff/staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/delete-transactions/<int:transaction_id>/', views.delete_transaction, name='delete_transactions'),
    path('staff/view-transactions/<int:transaction_id>/', views.view_transaction, name='view_transactions'),
    path('staff/product/', views.product, name='staff_product'),
    path('staff/categories/', views.categories, name='categories'),
    path('staff/supplier', views.supplier, name='supplier'),
    path('staff/stock-in', views.stock_in, name='stock_in'),
]