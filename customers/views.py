from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404

from activities.models import Activity
from bookings.models import Booking, BookingActivity
from commissions.models import CommissionRecord, CommissionTimeline
from registrations.models import Registration, RegistrationTimeline
from django.db.models import Sum, Count, Q
from .models import Customer, CustomerProperty
from .forms import CustomerForm
from accounts.decorators import role_required
from notifications.models import Notification
from payments.models import Payment

@role_required(["admin", "manager", "sales"])
def customer_list(request):

    query = request.GET.get("q", "")

    customers = Customer.objects.all()

    if query:

        customers = customers.filter(
            customer_name__icontains=query
        )

    return render(
        request,
        "customers/customer_list.html",
        {
            "customers": customers,
            "query": query,
        },
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


@role_required(["admin", "manager", "sales"])
def customer_profile(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    properties = customer.properties.select_related(
        "project",
        "plot",
        "assigned_employee",
        "assigned_team",
        "booking"
    )

    return render(
        request,
        "customers/customer_profile.html",
        {
            "customer": customer,
            "properties": properties,
        },
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

@role_required(["admin", "accounts", "manager", "sales"])
def customer_workspace(request, customer_id):

    customer = get_object_or_404(
        Customer.objects.select_related(
            "created_by",
            "updated_by",
        ).prefetch_related(
            Prefetch(
                "properties",
                queryset=CustomerProperty.objects.select_related(
                    "booking",
                    "project",
                    "plot",
                    "assigned_employee",
                    "assigned_team",
                ),
            )
        ),
        pk=customer_id,
    )

    customer_properties = customer.properties.all()

    bookings = Booking.objects.select_related(
        "customer_property",
        "project",
        "plot",
        "assigned_employee",
        "assigned_team",
    ).filter(
        customer_property__customer=customer
    ).order_by(
        "-booking_date"
    )

    payments = Payment.objects.select_related(
        "booking",
        "booking__project",
    ).filter(
        booking__customer_property__customer=customer
    ).order_by(
        "-payment_date"
    )

    total_bookings = bookings.count()

    total_payments_amount = payments.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_outstanding_amount = customer_properties.aggregate(
        total=Sum("pending_amount")
    )["total"] or 0

    total_properties = customer_properties.count()

    commissions = CommissionRecord.objects.select_related(
        "booking",
        "customer",
        "project",
    ).filter(
        customer=customer
    ).order_by(
        "-created_at"
    )

    registrations = Registration.objects.select_related(
        "booking",
        "customer",
        "booking__project",
    ).filter(
        customer=customer
    ).order_by(
        "-registration_date"
    )

    recent_activities = Activity.objects.select_related(
        "booking",
        "payment",
        "commission",
        "registration",
        "employee",
        "created_by",
    ).filter(
        customer=customer
    ).order_by(
        "-created_at"
    )[:50]

    context = {

        "customer": customer,

        "customer_properties": customer_properties,

        "total_bookings": total_bookings,

        "total_payments_amount": total_payments_amount,

        "total_outstanding_amount": total_outstanding_amount,

        "total_properties": total_properties,

        "bookings": bookings,

        "payments": payments,

        "commissions": commissions,

        "registrations": registrations,

        "recent_activities": recent_activities,

    }

    return render(

        request,

        "customers/customer_workspace.html",

        context,

    )