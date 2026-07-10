from django.shortcuts import render
from django.db.models import Sum
from accounts.decorators import role_required

from employees.models import Employee
from leads.models import Lead
from customers.models import Customer
from bookings.models import Booking
from payments.models import Payment
from commissions.models import Commission

from dashboard.services.dashboard_service import DashboardService


# ==========================================================
# Admin Dashboard
# ==========================================================

@role_required(['admin', 'manager'])
def dashboard_home(request):

    context = DashboardService.get_dashboard_data()

    return render(
        request,
        "dashboard/home.html",
        context
    )


# ==========================================================
# Sales Dashboard
# ==========================================================

@role_required(['sales'])
def sales_dashboard(request):

    employee = Employee.objects.filter(
        email=request.user.email
    ).first()

    if not employee:

        return render(
            request,
            "dashboard/sales.html",
            {
                "error": "Employee profile not found"
            }
        )

    my_leads = Lead.objects.filter(
        assigned_employee=employee
    )

    my_bookings = Booking.objects.filter(
        assigned_employee=employee
    )

    my_customers = Customer.objects.filter(
        booking__assigned_employee=employee
    )

    my_payments = Payment.objects.filter(
        booking__assigned_employee=employee
    )

    context = {

        "my_leads_count":
            my_leads.count(),

        "my_customers_count":
            my_customers.count(),

        "my_bookings_count":
            my_bookings.count(),

        'my_revenue': (
            my_payments.aggregate(
                total=Sum("amount")
            )["total"] or 0
        ),

        "recent_leads":
            my_leads.order_by("-id")[:5],

        "recent_bookings":
            my_bookings.order_by("-id")[:5],

    }

    return render(
        request,
        "dashboard/sales.html",
        context
    )


# ==========================================================
# Accounts Dashboard
# ==========================================================

@role_required(['accounts'])
def accounts_dashboard(request):

    context = {

        "total_payments":
            Payment.objects.count(),

        "total_revenue":
            DashboardService.get_dashboard_data()["total_revenue"],

        "pending_commissions":
            Commission.objects.filter(
                status="generated"
            ).count(),

        "recent_payments":
            Payment.objects.order_by("-payment_date")[:5],

    }

    return render(
        request,
        "dashboard/accounts.html",
        context
    )