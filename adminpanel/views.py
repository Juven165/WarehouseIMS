from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from staff.models import Product, StockTransaction
from django.db.models import F

User = get_user_model()

@login_required
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

    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_staff': total_staff,
        'total_supplier': total_supplier,
        'pending_approvals': pending_approvals,
        'low_stock_count': low_stock_count,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)