from django.shortcuts import render
from employees.models import Employee
from leads.models import Lead
from customers.models import Customer
from bookings.models import Booking
from payments.models import Payment
from commissions.models import Commission
from projects.models import Plot


def dashboard_home(request):
    context = {
        'total_employees': Employee.objects.count(),
        'total_leads': Lead.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_payments': Payment.objects.count(),

        'total_revenue': sum(
            payment.amount for payment in Payment.objects.all()
        ),

        'pending_commissions': Commission.objects.filter(
            status='pending'
        ).count(),

        'available_plots': Plot.objects.filter(
            status='available'
        ).count(),

        'booked_plots': Plot.objects.filter(
            status='booked'
        ).count(),

        'registered_plots': Plot.objects.filter(
            status='registered'
        ).count(),
    }

    return render(request, 'dashboard/home.html', context)