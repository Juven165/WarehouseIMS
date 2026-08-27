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
from django.contrib.messages.context_processors import messages


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
            delivery.staff = request.user
            delivery.save()

            messages.success(request, "Delivery submitted successfully!")
            return redirect('submit_inventory')
    else:
        form = SubmitInventoryForm()

    return render(request, 'supplier/submit_inventory.html', {
        'form': form
    })