from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from staff.models import Product, StockTransaction, Category, Supplier
from .forms import StockInForm, StockOutForm, AdjustmentForm
from datetime import datetime
from django.utils.timezone import make_aware


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

    recent_transactions = (
        StockTransaction.objects
        .select_related(
            'product',
            'product__supplier',
            'supplier',
            'staff'
        )
        .order_by('-transaction_date')[:5]
    )

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
        'suppliers': suppliers,
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

@login_required
def stock_in(request):
    recent_transactions = StockTransaction.objects.filter(
        transaction_type="Stock In"
    ).select_related('product', 'supplier').order_by('-transaction_date')[:10]

    products = Product.objects.all()
    suppliers = Supplier.objects.filter(is_active=True)

    if request.method == 'POST':
        form = StockInForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = "Stock In"
            transaction.staff = request.user
            transaction.save()

            # Update stock
            product = transaction.product
            product.current_stock += transaction.quantity
            product.save()

            messages.success(request, f"Stock In successful for {product.name}!")
            return redirect('stock_in')
    else:
        form = StockInForm()

    context = {
        'form': form,
        'recent_transactions': recent_transactions,
        'products': products,
        'suppliers': suppliers,
    }
    return render(request, 'staff/stock_in.html', context)

@login_required
def stock_out(request):
    recent_stock_out = (
        StockTransaction.objects
        .filter(transaction_type="Stock Out")
        .select_related('product', 'staff')
        .order_by('-transaction_date')[:10]
    )

    if request.method == 'POST':
        form = StockOutForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = "Stock Out"
            transaction.staff = request.user
            transaction.save()

            product = transaction.product
            product.current_stock -= transaction.quantity
            product.save()

            messages.success(request, 'Stock successfully deducted!')
            return redirect('stock_out')
    else:
        form = StockOutForm()

    context = {
        'form': form,
        'recent_stock_out_trans': recent_stock_out,
    }
    return render(request, 'staff/stock_out.html', context)

@login_required
def adjustment(request):
    recent_adjustments = (
        StockTransaction.objects
        .filter(transaction_type="Adjustment")
        .select_related('product', 'staff')
        .order_by('-transaction_date')[:10]
    )

    if request.method == 'POST':
        form = AdjustmentForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = "Adjustment"
            transaction.staff = request.user

            product = transaction.product
            quantity = transaction.quantity

            if transaction.adjustment_type == "Increase":
                product.current_stock += quantity
                transaction.save()
                product.save()
                messages.success(request, 'Stock successfully increased!')
                return redirect('adjustment')

            else:  # Decrease
                if quantity > product.current_stock:
                    form.add_error('quantity', f'Insufficient stock. Only {product.current_stock} available.')
                else:
                    product.current_stock -= quantity
                    transaction.save()
                    product.save()
                    messages.success(request, 'Stock successfully decreased!')
                    return redirect('adjustment')
    else:
        form = AdjustmentForm()

    context = {
        'recent_adjustments': recent_adjustments,
        'form': form,
    }
    return render(request, 'staff/adjustments.html', context)

@login_required
def stock_transaction_history(request):
    transactions = StockTransaction.objects.select_related(
        'staff', 'supplier', 'product'
    ).order_by('-transaction_date')

    query = request.GET.get('q', '').strip()
    transaction_type = request.GET.get('transaction_type', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    if query:
        transactions = transactions.filter(
            Q(product__name__icontains=query) |
            Q(product__sku__icontains=query)
        )

    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    if date_from:
        try:
            date_from_obj = make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
            transactions = transactions.filter(transaction_date__date__gte=date_from_obj.date())
        except ValueError:
            pass

    if date_to:
        try:
            date_to_obj = make_aware(datetime.strptime(date_to, '%Y-%m-%d'))
            transactions = transactions.filter(transaction_date__date__lte=date_to_obj.date())
        except ValueError:
            pass

    return render(request, "staff/transaction_history.html", {
        "transactions": transactions,
        "query": query,
        "selected_type": transaction_type,
        "date_from": date_from,
        "date_to": date_to,
    })