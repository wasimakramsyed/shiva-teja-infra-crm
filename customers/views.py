from django.shortcuts import render
from .models import Customer
from accounts.decorators import role_required


@role_required(['admin', 'manager', 'sales'])
def customer_list(request):
    query = request.GET.get('q')
    assigned_filter = request.GET.get('assigned_to')

    customers = Customer.objects.all()

    # Search by customer name
    if query:
        customers = customers.filter(
            customer_name__icontains=query
        )

    # Filter by assigned employee
    if assigned_filter:
        customers = customers.filter(
            assigned_to__id=assigned_filter
        )

    return render(
        request,
        'customers/customer_list.html',
        {
            'customers': customers,
            'query': query,
            'assigned_filter': assigned_filter
        }
    )