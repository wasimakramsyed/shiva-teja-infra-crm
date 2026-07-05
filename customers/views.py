from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm
from accounts.decorators import role_required
from notifications.models import Notification
from commissions.models import Commission


@role_required(['admin', 'manager', 'sales'])
def customer_list(request):
    query = request.GET.get('q')
    ownership_filter = request.GET.get('ownership_status')

    customers = Customer.objects.all()

    if query:
        customers = customers.filter(
            customer_name__icontains=query
        )

    if ownership_filter:
        customers = customers.filter(
            ownership_status=ownership_filter
        )

    return render(
        request,
        'customers/customer_list.html',
        {
            'customers': customers,
            'query': query,
            'ownership_filter': ownership_filter
        }
    )


@role_required(['admin', 'sales'])
def create_customer(request):
    form = CustomerForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        customer = form.save()

        Notification.objects.create(
            message=(
                f"Customer created: "
                f"{customer.customer_id}"
            )
        )

        return redirect('/customers/')

    return render(
        request,
        'customers/create_customer.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'manager', 'sales'])
def customer_profile(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    payments = customer.booking.payments.all()

    commissions = Commission.objects.filter(
        payment__booking=customer.booking
    )

    return render(
        request,
        'customers/customer_profile.html',
        {
            'customer': customer,
            'payments': payments,
            'commissions': commissions
        }
    )


@role_required(['admin', 'sales'])
def edit_customer(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    form = CustomerForm(
        request.POST or None,
        request.FILES or None,
        instance=customer
    )

    if form.is_valid():
        form.save()

        Notification.objects.create(
            message=(
                f"Customer updated: "
                f"{customer.customer_id}"
            )
        )

        return redirect('/customers/')

    return render(
        request,
        'customers/create_customer.html',
        {
            'form': form
        }
    )