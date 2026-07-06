from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .models import Booking
from .forms import BookingForm

from leads.models import Lead
from projects.models import Plot
from payments.models import Payment
from notifications.models import Notification
from accounts.decorators import role_required


# ==========================================================
# Booking List
# ==========================================================
@role_required(['admin', 'manager', 'sales'])
def booking_list(request):

    query = request.GET.get('q', '')
    status_filter = request.GET.get('status')

    bookings = Booking.objects.select_related(
        'project',
        'plot',
        'lead'
    )

    if query:
        bookings = bookings.filter(
            Q(booking_id__icontains=query) |
            Q(booked_client_name__icontains=query) |
            Q(mobile_number__icontains=query) |
            Q(project__project_name__icontains=query) |
            Q(plot__plot_number__icontains=query)
        )

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(
        request,
        'bookings/booking_list.html',
        {
            'bookings': bookings,
            'query': query,
            'status_filter': status_filter
        }
    )


# ==========================================================
# Create Booking
# ==========================================================
@role_required(['admin', 'manager', 'sales'])
def create_booking(request):

    form = BookingForm(
        request.POST or None,
        request.FILES or None
    )

    lead_id = request.GET.get('lead')

    if lead_id and request.method != 'POST':
        try:
            lead = Lead.objects.get(id=lead_id)

            form.initial['lead'] = lead
            form.initial['booked_client_name'] = lead.lead_name
            form.initial['mobile_number'] = lead.mobile_number
            form.initial['project'] = lead.project

        except Lead.DoesNotExist:
            pass

    if request.method == 'POST':

        if form.is_valid():

            try:

                booking = form.save(commit=False)
                
                print("Lead =", booking.lead)
                print("Lead ID =", booking.lead_id)

                booking.full_clean()

                booking.save()

                # Update plot status
                booking.plot.status = 'booked'
                booking.plot.save()

                # Update lead
                if booking.lead:
                    booking.lead.status = 'converted'
                    booking.lead.save()

                # Notification
                Notification.objects.create(
                    message=(
                        f"Booking Created : "
                        f"{booking.booking_id}"
                    )
                )

                messages.success(
                    request,
                    f"Booking {booking.booking_id} created successfully."
                )

                return redirect(
                    'booking_profile',
                    booking_id=booking.id
                )

            except ValidationError as e:

                form.add_error(
                    None,
                    e
                )

                messages.error(
                    request,
                    "Please correct the errors below."
                )

        else:

            print(form.errors)

            messages.error(
                request,
                "Please correct the errors below."
            )

    return render(
        request,
        'bookings/create_booking.html',
        {
            'form': form
        }
    )


# ==========================================================
# Booking Profile
# ==========================================================
@role_required(['admin', 'manager', 'sales'])
def booking_profile(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    payments = Payment.objects.filter(
        booking=booking
    ).order_by('-payment_date')

    total_paid = (
        booking.advance_amount +
        sum(
            payment.amount
            for payment in payments
        )
    )

    pending = booking.booking_amount - total_paid

    return render(
        request,
        'bookings/booking_profile.html',
        {
            'booking': booking,
            'payments': payments,
            'total_paid': total_paid,
            'pending': pending
        }
    )


# ==========================================================
# Edit Booking
# ==========================================================
@role_required(['admin', 'sales'])
def edit_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    form = BookingForm(
        request.POST or None,
        request.FILES or None,
        instance=booking
    )

    if request.method == 'POST':

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Booking updated successfully."
            )

            return redirect(
                'booking_profile',
                booking_id=booking.id
            )

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    return render(
        request,
        'bookings/create_booking.html',
        {
            'form': form
        }
    )


# ==========================================================
# AJAX Load Plots
# ==========================================================
def load_plots(request):

    project_id = request.GET.get('project_id')

    plots = Plot.objects.filter(
        project_id=project_id,
        status='available'
    ).values(
        'id',
        'plot_number'
    ).order_by(
        'plot_number'
    )

    return JsonResponse(
        list(plots),
        safe=False
    )