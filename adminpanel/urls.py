from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-transaction/<int:trans_id>/', views.delete_transactions, name='delete_transaction'),
    path('view-transaction/<int:trans_id>/', views.view_transactions, name='view_transaction'),
    path('user-list/', views.user_list, name='user_list'),
    path('activate/<int:user_id>/', views.activate, name='activate'),
    path('deactivate/<int:user_id>/', views.deactivate, name='deactivate'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('product-list/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('product-details/<int:pk>/', views.product_details, name='product_details'),
    path('category/', views.category_list, name='category_list'),
    path('category-list/<int:pk>/', views.category_details, name='category_details'),

]