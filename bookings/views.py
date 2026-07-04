from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .models import Booking
from .forms import BookingForm
from accounts.decorators import role_required
from notifications.models import Notification


@role_required(['admin', 'manager', 'sales'])
def booking_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    bookings = Booking.objects.all()

    if query:
        bookings = bookings.filter(
            booked_client_name__icontains=query
        )

    if status_filter:
        bookings = bookings.filter(
            status=status_filter
        )

    return render(
        request,
        'bookings/booking_list.html',
        {
            'bookings': bookings,
            'query': query,
            'status_filter': status_filter
        }
    )


@role_required(['sales'])
def create_booking(request):
    form = BookingForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        try:
            booking = form.save(commit=False)

            # Auto-fill booked client from lead
            booking.booked_client_name = (
                booking.lead.lead_name
            )

            booking.mobile_number = (
                booking.lead.mobile_number
            )

            booking.full_clean()
            booking.save()

            Notification.objects.create(
                message=(
                    f"New booking created: "
                    f"{booking.booking_id}"
                )
            )

            return redirect('/bookings/')

        except ValidationError as e:
            form.add_error(None, e)

    return render(
        request,
        'bookings/create_booking.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'manager', 'sales'])
def booking_profile(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    return render(
        request,
        'bookings/booking_profile.html',
        {
            'booking': booking
        }
    )


@role_required(['sales'])
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

    if form.is_valid():
        form.save()
        return redirect('/bookings/')

    return render(
        request,
        'bookings/create_booking.html',
        {
            'form': form
        }
    )