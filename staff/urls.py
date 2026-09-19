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
    path('staff/stock-out', views.stock_out, name='stock_out'),
    path('staff/adjustment', views.adjustment, name='adjustment'),
    path('staff/transaction-history/', views.stock_transaction_history, name='transactions_history'),
    path('staff/pending-approval/', views.pending_approval, name='pending_approval'),
    path('staff/approve-transaction/<int:pk>/', views.approve_transaction, name='approve_transaction'),
    path('staff/reject-transaction/<int:pk>/', views.reject_transaction, name='reject_transaction'),
    path('staff/add-product/', views.add_product, name='add_product'),
    path('staff/add-category/', views.add_category, name='add_category'),
    path('staff/view-trans/<int:pk>/', views.view_trans, name='view_trans'),
    path('staff/delete-trans/<int:pk>/', views.delete_trans, name='delete_trans'),
    path('staff/product-detail/<int:pk>/', views.view_product_detail, name='product_detail'),
    path('staff/update-product/<int:pk>/', views.update_product, name='update_product'),
]