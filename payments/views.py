from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Payment
from .forms import PaymentForm
from accounts.decorators import role_required
from notifications.models import Notification
from django.http import HttpResponse
from reportlab.pdfgen import canvas


@role_required(['admin', 'accounts'])
def generate_payment_receipt(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; '
        f'filename="{payment.receipt_number}.pdf"'
    )

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(
        200,
        800,
        "Payment Receipt"
    )

    p.setFont("Helvetica", 12)

    p.drawString(
        50,
        750,
        f"Receipt Number: {payment.receipt_number}"
    )

    p.drawString(
        50,
        720,
        f"Payment ID: {payment.payment_id}"
    )

    p.drawString(
        50,
        690,
        f"Booking ID: {payment.booking.booking_id}"
    )

    p.drawString(
        50,
        660,
        f"Customer: {payment.booking.booked_client_name}"
    )

    p.drawString(
        50,
        630,
        f"Project: {payment.booking.project.project_name}"
    )

    p.drawString(
        50,
        600,
        f"Plot: {payment.booking.plot.plot_number}"
    )

    p.drawString(
        50,
        570,
        f"Amount Paid: ₹{payment.amount}"
    )

    p.drawString(
        50,
        540,
        f"Payment Date: {payment.payment_date}"
    )

    p.drawString(
        50,
        510,
        f"Payment Mode: {payment.payment_mode}"
    )

    p.drawString(
        50,
        480,
        f"Status: {payment.status}"
    )

    p.drawString(
        50,
        420,
        "Authorized Signature"
    )

    p.line(
        50,
        430,
        200,
        430
    )

    p.showPage()
    p.save()

    return response

@role_required(['admin', 'accounts'])
def payment_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    payments = Payment.objects.all()

    if query:
        payments = payments.filter(
            payment_id__icontains=query
        )

    if status_filter:
        payments = payments.filter(
            status=status_filter
        )

    return render(
        request,
        'payments/payment_list.html',
        {
            'payments': payments,
            'query': query,
            'status_filter': status_filter
        }
    )


@role_required(['accounts'])
def create_payment(request):
    booking_id = request.GET.get('booking')

    form = PaymentForm(
        request.POST or None,
        request.FILES or None,
        booking_id=booking_id
    )

    if request.method == 'POST':
        if form.is_valid():
            try:
                payment = form.save(commit=False)
                payment.full_clean()
                payment.save()

                Notification.objects.create(
                    message=(
                        f"Payment received: "
                        f"{payment.payment_id}"
                    )
                )

                messages.success(
                    request,
                    f"Payment {payment.payment_id} added successfully."
                )

                return redirect(
                    f'/bookings/{payment.booking.id}/'
                )

            except ValidationError as e:
                form.add_error(None, e)

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    return render(
        request,
        'payments/create_payment.html',
        {
            'form': form
        }
    )


@role_required(['admin', 'accounts'])
def payment_profile(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    return render(
        request,
        'payments/payment_profile.html',
        {
            'payment': payment
        }
    )


@role_required(['accounts'])
def edit_payment(request, payment_id):
    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    form = PaymentForm(
        request.POST or None,
        request.FILES or None,
        instance=payment
    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Payment updated successfully."
            )

            return redirect('/payments/')
        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    return render(
        request,
        'payments/create_payment.html',
        {
            'form': form
        }
    )