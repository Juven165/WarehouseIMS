from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Q, Count
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from staff.models import Product, StockTransaction, Category, Supplier

@login_required
def staff_dashboard(request):
    products = Product.objects.all()
    product_transactions = StockTransaction.objects.all()

    total_products = products.count()

    total_stock = products.aggregate(
        total=Sum('current_stock')
    )['total'] or 0

    low_stock_products = products.filter(
        current_stock__lte=F('low_stock'),
        current_stock__gt=0
    ).count()

    out_of_stock = products.filter(
        current_stock=0
    ).count()

    today = timezone.localdate()

    todays_transactions = product_transactions.filter(
        transaction_date__date=today
    ).count()

    recent_transactions = product_transactions.select_related(
        'product',
        'product__supplier'
    ).order_by('-transaction_date')[:5]

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        'todays_transactions': todays_transactions,
        'recent_transactions': recent_transactions,
    }

    return render(
        request,
        'dashboard/staff_dashboard.html',
        context
    )

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(
        StockTransaction,
        id=transaction_id
    )

    transaction.delete()

    messages.success(
        request,
        'Transaction deleted successfully.'
    )
    return redirect('staff_dashboard')

@login_required
def view_transaction(request, transaction_id):
    transaction = get_object_or_404(
        StockTransaction,
        id=transaction_id
    )

    return render(
        request,
        'staff/view_transaction.html',
        {'transaction': transaction}
    )

@login_required
def product(request):
    products = Product.objects.all()
    query = request.GET.get('q', '').strip()

    if query:
        products = products.filter(Q(sku__icontains=query) | Q(name__icontains=query))

    return render(request, 'staff/product.html', {'products': products})

@login_required
def categories(request):
    category = Category.objects.all()
    products = Product.objects.all()

    total_products = products.count()

    return render(request, 'staff/categories.html', {
        'category': category,
        'total_products': total_products,
    })

@login_required
def supplier(request):
    suppliers = Supplier.objects.all()

    total_suppliers = suppliers.count()

    return render(request, 'staff/supplier.html', {
        'suppliers': supplier,
        'total_suppliers': total_suppliers
    })

@login_required
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    supplier_name = supplier.name
    supplier.delete()

    messages.success(request, f"Supplier '{supplier_name}' deleted successfully.")

    return redirect('supplier')

@login_required
def view_supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    return render(request, 'staff/supplier_detail.html', {'supplier': supplier})
