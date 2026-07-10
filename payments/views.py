from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from reportlab.pdfgen import canvas

from .models import Payment
from .forms import PaymentForm
from .services.payment_service import PaymentService

from accounts.decorators import role_required


@role_required(['admin', 'accounts'])
def create_payment(request):

    booking_id = request.GET.get("booking")

    form = PaymentForm(
        request.POST or None,
        booking_id=booking_id
    )

    if request.method == "POST":

        if form.is_valid():

            try:

                payment = PaymentService.receive_payment(form)

                messages.success(
                    request,
                    f"Payment of ₹{payment.amount} received successfully."
                )

                return redirect(
                    "booking_profile",
                    booking_id=payment.booking.id
                )

            except ValidationError as e:

                messages.error(
                    request,
                    str(e)
                )

        else:

            messages.error(
                request,
                "Please correct the highlighted errors."
            )
    print("FORM CLASS:", type(form))
    print("PAYMENT MODE CHOICES IN VIEW:", list(form.fields["payment_mode"].choices))

    return render(
        request,
        "payments/create_payment.html",
        {
            "form": form
        }
    )


@role_required(['admin', 'accounts'])
def payment_list(request):

    query = request.GET.get("q")

    payments = Payment.objects.select_related(
        "booking",
        "booking__project",
        "booking__plot"
    )

    if query:

        payments = payments.filter(
            payment_id__icontains=query
        )

    return render(
        request,
        "payments/payment_list.html",
        {
            "payments": payments,
            "query": query
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
        "payments/payment_profile.html",
        {
            "payment": payment
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
        instance=payment
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Payment updated successfully."
            )

            return redirect(
                "payment_profile",
                payment_id=payment.id
            )

    return render(
        request,
        "payments/create_payment.html",
        {
            "form": form
        }
    )


@role_required(['admin', 'accounts'])
def generate_payment_receipt(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; filename="{payment.receipt_number}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "PAYMENT RECEIPT")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        760,
        f"Receipt No : {payment.receipt_number}"
    )

    pdf.drawString(
        50,
        735,
        f"Payment ID : {payment.payment_id}"
    )

    pdf.drawString(
        50,
        710,
        f"Booking ID : {payment.booking.booking_id}"
    )

    pdf.drawString(
        50,
        685,
        f"Customer : {payment.booking.booked_client_name}"
    )

    pdf.drawString(
        50,
        660,
        f"Project : {payment.booking.project.project_name}"
    )

    pdf.drawString(
        50,
        635,
        f"Plot : {payment.booking.plot.plot_number}"
    )

    pdf.drawString(
        50,
        610,
        f"Amount : ₹ {payment.amount}"
    )

    pdf.drawString(
        50,
        585,
        f"Date : {payment.payment_date}"
    )

    pdf.drawString(
        50,
        560,
        f"Mode : {payment.payment_mode}"
    )

    pdf.drawString(
        50,
        520,
        "Authorized Signature"
    )

    pdf.line(
        50,
        530,
        180,
        530
    )

    pdf.showPage()
    pdf.save()

    return response