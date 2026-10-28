from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import F, Q

from staff.forms import AddProductForm
from staff.models import Product, StockTransaction, Category

User = get_user_model()

@staff_member_required
def admin_dashboard(request):
    # admin role
    if getattr(request.user, 'role', None) != 'admin':
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'Access denied.')
        return redirect('login')

    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_staff = User.objects.filter(role='staff').count()
    total_supplier = User.objects.filter(role='supplier').count()
    pending_approvals = StockTransaction.objects.filter(status='Pending').count()

    low_stock_count = Product.objects.filter(
        current_stock__lte=F('low_stock')
    ).count()

    recent_transactions = (
        StockTransaction.objects
        .select_related('product', 'staff', 'supplier')
        .order_by('-transaction_date')[:10]
    )

    recent_users = (
        User.objects
        .order_by('-date_joined')[:8]
    )

    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_staff': total_staff,
        'total_supplier': total_supplier,
        'pending_approvals': pending_approvals,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
        'recent_users': recent_users,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@staff_member_required
def delete_transactions(request, trans_id):
    obj = get_object_or_404(StockTransaction, id=trans_id)
    obj.delete()
    messages.success(request, 'Transaction deleted.')
    return redirect('admin_dashboard')

@staff_member_required
def view_transactions(request, trans_id):
    transactions = get_object_or_404(StockTransaction, id=trans_id)

    return render(request, 'admin/transaction_detail.html', {'transactions': transactions})

@staff_member_required
def user_list(request):
    query = request.GET.get('q', '').strip()
    role = request.GET.get('role', '').strip()

    users = User.objects.all().select_related('profile').order_by('-date_joined')

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    if role:
        users = users.filter(role=role)

    return render(request, 'admin/user_list.html', {
        'users': users,
        'query': query,
        'selected_role': role,
    })

@staff_member_required
def activate(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser or user.role == 'admin':
        messages.error(request, 'You cannot modify an administrator account.')
        return redirect('user_list')

    if user == request.user:
        messages.error(request, 'You cannot activate/deactivate your own account.')
        return redirect('user_list')

    user.is_active = True
    user.save()
    messages.success(request, f'"{user.username}" is now active.')
    return redirect('user_list')


@staff_member_required
def deactivate(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser or user.role == 'admin':
        messages.error(request, 'You cannot modify an administrator account.')
        return redirect('user_list')

    if user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('user_list')

    user.is_active = False
    user.save()
    messages.warning(request, f'"{user.username}" has been deactivated.')
    return redirect('user_list')

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        messages.error(request, 'You cannot delete an administrator account.')
        return redirect('user_list')

    user.delete()
    messages.success(request, f"{user.username} deleted successfully!")
    return redirect('user_list')

@staff_member_required  # or @login_required
def product_list(request):
    products = Product.objects.select_related('category', 'supplier').order_by('-created_at')
    categories = Category.objects.filter(is_active=True).order_by('name')

    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    if status == 'in_stock':
        products = products.filter(current_stock__gt=F('low_stock'))
    elif status == 'low_stock':
        products = products.filter(
            current_stock__gt=0,
            current_stock__lte=F('low_stock')
        )
    elif status == 'out_of_stock':
        products = products.filter(current_stock=0)

    return render(request, 'admin/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'selected_status': status,
    })

@staff_member_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f"{product.name} added successfully!")
            return redirect('product_list')
    else:
        form = AddProductForm()
    return render(request, 'admin/add_product.html', {'form': form})