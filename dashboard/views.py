from django.shortcuts import render
from employees.models import Employee
from leads.models import Lead
from customers.models import Customer
from bookings.models import Booking
from payments.models import Payment
from commissions.models import Commission
from projects.models import Plot
from accounts.decorators import role_required


@role_required(['admin', 'manager'])
def dashboard_home(request):
    context = {
        # Main Stats
        'total_employees': Employee.objects.count(),
        'total_leads': Lead.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_payments': Payment.objects.count(),

        # Revenue
        'total_revenue': sum(
            payment.amount
            for payment in Payment.objects.all()
        ),

        # Commission
        'pending_commissions': Commission.objects.filter(
            status='pending'
        ).count(),

        # Plot Status
        'available_plots': Plot.objects.filter(
            status='available'
        ).count(),

        'booked_plots': Plot.objects.filter(
            status='booked'
        ).count(),

        'registered_plots': Plot.objects.filter(
            status='registered'
        ).count(),

        # Recent Activity
        'recent_leads': Lead.objects.order_by('-id')[:5],
        'recent_bookings': Booking.objects.order_by('-id')[:5],
        'recent_payments': Payment.objects.order_by('-id')[:5],

        # Chart Data
        'new_leads': Lead.objects.filter(
            status='new'
        ).count(),

        'converted_leads': Lead.objects.filter(
            status='converted'
        ).count(),
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )


@role_required(['sales'])
def sales_dashboard(request):
    # Safe employee lookup
    employee = Employee.objects.filter(
        email=request.user.email
    ).first()

    # If employee not found
    if not employee:
        return render(
            request,
            'dashboard/sales.html',
            {
                'error': 'Employee profile not found'
            }
        )

    # Sales-specific data
    my_leads = Lead.objects.filter(
        assigned_employee=employee
    )

    my_customers = Customer.objects.filter(
        assigned_to=employee
    )

    my_bookings = Booking.objects.filter(
        customer__assigned_to=employee
    )

    my_payments = Payment.objects.filter(
        booking__customer__assigned_to=employee
    )

    context = {
        'my_leads_count': my_leads.count(),
        'my_customers_count': my_customers.count(),
        'my_bookings_count': my_bookings.count(),

        'my_revenue': sum(
            payment.amount
            for payment in my_payments
        ),

        'recent_leads': my_leads.order_by('-id')[:5],
        'recent_bookings': my_bookings.order_by('-id')[:5],
    }

    return render(
        request,
        'dashboard/sales.html',
        context
    )


@role_required(['accounts'])
def accounts_dashboard(request):
    context = {
        'total_payments': Payment.objects.count(),

        'total_revenue': sum(
            payment.amount
            for payment in Payment.objects.all()
        ),

        'pending_commissions': Commission.objects.filter(
            status='pending'
        ).count(),

        'recent_payments': Payment.objects.order_by('-id')[:5],
    }

    return render(
        request,
        'dashboard/accounts.html',
        context
    )