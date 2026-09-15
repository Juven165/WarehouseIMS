from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from staff.models import StockTransaction, Supplier
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from staff.models import Product
from staff.forms import SubmitInventoryForm
from datetime import datetime
from django.contrib import messages


class SupplierDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/supplier_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        supplier = Supplier.objects.filter(email=self.request.user.email).first()

        if supplier:
            transactions = StockTransaction.objects.filter(
                supplier=supplier,
                transaction_type="Stock In"
            ).select_related('product')
        else:
            transactions = StockTransaction.objects.none()

        context['supplier'] = supplier
        context['total_deliveries'] = transactions.count()
        context['pending_count'] = transactions.filter(status='Pending').count()
        context['approved_count'] = transactions.filter(status='Approved').count()
        context['rejected_count'] = transactions.filter(status='Rejected').count()
        context['recent_deliveries'] = transactions.order_by('-transaction_date')[:10]

        return context

@login_required
def edit_delivery(request, pk):
    delivery = get_object_or_404(
        StockTransaction,
        pk=pk,
        status="Pending"
    )

    supplier = getattr(request.user, 'supplier_profile', None)
    if supplier and delivery.supplier != supplier:
        messages.error(request, "You cannot edit this delivery.")
        return redirect('supplier_dashboard')

    if request.method == 'POST':
        form = SubmitInventoryForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery updated successfully!")
            return redirect('supplier_dashboard')
    else:
        form = SubmitInventoryForm(instance=delivery)

    return render(request, 'supplier/edit_delivery.html', {
        'form': form,
        'delivery': delivery
    })

class SupplierMyDeliveries(LoginRequiredMixin, TemplateView):
    template_name = 'supplier/supplier_my_deliveries.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        supplier = Supplier.objects.filter(email=self.request.user.email).first()

        if supplier:
            transactions = StockTransaction.objects.filter(
                supplier=supplier,
                transaction_type="Stock In"
            ).select_related('product').order_by('-transaction_date')
        else:
            transactions = StockTransaction.objects.none()

        # This Month filter
        now = timezone.now()
        this_month = transactions.filter(
            transaction_date__year=now.year,
            transaction_date__month=now.month
        )

        context['supplier'] = supplier
        context['transactions'] = transactions
        context['deliveries_this_month'] = this_month.count()
        context['pending_count'] = transactions.filter(status='Pending').count()
        context['approved_count'] = transactions.filter(status='Approved').count()
        context['rejected_count'] = transactions.filter(status='Rejected').count()
        context['recent_deliveries'] = transactions.order_by('-transaction_date')[:10]

        return context


@login_required
def submit_inventory(request):
    if request.method == 'POST':
        form = SubmitInventoryForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.transaction_type = "Stock In"
            delivery.status = "Pending"

            if hasattr(request.user, 'supplier_profile'):
                delivery.supplier = request.user.supplier_profile

            delivery.save()

            messages.success(request, "Delivery submitted successfully!")
            return redirect('submit_inventory')
    else:
        form = SubmitInventoryForm()

    return render(request, 'supplier/submit_inventory.html', {
        'form': form
    })

@login_required
def view_details(request, product_id):
    reports = get_object_or_404(StockTransaction, id=product_id)

    return render(request, 'supplier/view_details.html', {'reports': reports})

@login_required
def my_report(request):
    supplier = Supplier.objects.filter(email=request.user.email).first()

    if supplier:
        reports = (
            StockTransaction.objects
            .filter(supplier=supplier, transaction_type="Stock In")
            .select_related('product')
            .order_by('-transaction_date')
        )
    else:
        reports = StockTransaction.objects.none()

    return render(request, 'supplier/my_report.html', {
        'reports': reports
    })

@login_required
def my_profile(request):
    pass