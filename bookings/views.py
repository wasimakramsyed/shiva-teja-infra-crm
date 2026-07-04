from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Booking
from .forms import BookingForm
from accounts.decorators import role_required
from notifications.models import Notification


@role_required(['admin', 'manager', 'sales'])
def booking_list(request):
    bookings = Booking.objects.all()
    return render(
        request,
        'bookings/booking_list.html',
        {'bookings': bookings}
    )


@role_required(['sales'])
def create_booking(request):
    form = BookingForm(request.POST or None)

    if form.is_valid():
        try:
            booking = form.save(commit=False)
            booking.full_clean()
            booking.save()

            Notification.objects.create(
                message=f"New booking created: {booking.booking_id}"
            )

            return redirect('/bookings/')

        except ValidationError as e:
            form.add_error(None, e)

    return render(
        request,
        'bookings/create_booking.html',
        {'form': form}
    )