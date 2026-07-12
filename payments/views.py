from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from reportlab.pdfgen import canvas

from .models import Payment
from .forms import PaymentForm
from .services.payment_service import PaymentService

from bookings.models import Booking

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

    return render(
        request,
        "payments/create_payment.html",
        {
            "form": form
        }
    )


from django.db.models import Sum, Q
from django.utils import timezone

from projects.models import Project


@role_required(['admin', 'accounts'])
def payment_list(request):

    query = request.GET.get("q", "")
    project = request.GET.get("project")
    plot = request.GET.get("plot")
    mode = request.GET.get("mode")

    payments = Payment.objects.select_related(
        "booking",
        "booking__project",
        "booking__plot"
    )

    # -------------------------
    # Search
    # -------------------------

    if query:

        payments = payments.filter(

            Q(payment_id__icontains=query) |

            Q(receipt_number__icontains=query) |

            Q(booking__booking_id__icontains=query) |

            Q(booking__booked_client_name__icontains=query) |

            Q(booking__mobile_number__icontains=query)

        )

    # -------------------------
    # Project Filter
    # -------------------------

    if project:

        payments = payments.filter(
            booking__project_id=project
        )

    # -------------------------
    # Plot Filter
    # -------------------------

    if plot:

        payments = payments.filter(
            booking__plot_id=plot
        )

    # -------------------------
    # Payment Mode
    # -------------------------

    if mode:

        payments = payments.filter(
            payment_mode=mode
        )

    # -------------------------
    # KPI Cards
    # -------------------------

    today = timezone.now().date()

    today_collection = Payment.objects.filter(
        payment_date=today
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    month_collection = Payment.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_collection = Payment.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {

        "payments": payments.order_by("-payment_date"),

        "query": query,

        "projects": Project.objects.all(),

        "today_collection": today_collection,

        "month_collection": month_collection,

        "total_collection": total_collection,

        "selected_project": project,

        "selected_plot": plot,

        "selected_mode": mode,

    }

    return render(

        request,

        "payments/payment_list.html",

        context

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

    pdf.drawString(50, 760, f"Receipt No : {payment.receipt_number}")
    pdf.drawString(50, 735, f"Payment ID : {payment.payment_id}")
    pdf.drawString(50, 710, f"Booking ID : {payment.booking.booking_id}")
    pdf.drawString(50, 685, f"Customer : {payment.booking.booked_client_name}")
    pdf.drawString(50, 660, f"Project : {payment.booking.project.project_name}")
    pdf.drawString(50, 635, f"Plot : {payment.booking.plot.plot_number}")
    pdf.drawString(50, 610, f"Amount : ₹ {payment.amount}")
    pdf.drawString(50, 585, f"Date : {payment.payment_date}")
    pdf.drawString(50, 560, f"Mode : {payment.payment_mode}")

    pdf.drawString(50, 520, "Authorized Signature")
    pdf.line(50, 530, 180, 530)

    pdf.showPage()
    pdf.save()

    return response


# ==========================================================
# AJAX Booking Payment Details
# ==========================================================

@role_required(['admin', 'accounts'])
def get_booking_payment_details(request):

    booking_id = request.GET.get("booking_id")

    if not booking_id:

        return JsonResponse(
            {
                "success": False
            }
        )

    try:

        booking = Booking.objects.get(id=booking_id)

    except Booking.DoesNotExist:

        return JsonResponse(
            {
                "success": False
            }
        )

    total_paid = booking.advance_amount + sum(
        payment.amount
        for payment in booking.payments.all()
    )

    remaining = booking.booking_amount - total_paid

    return JsonResponse({

        "success": True,

        "booking_id": booking.booking_id,

        "customer": booking.booked_client_name,

        "project": booking.project.project_name,

        "plot": booking.plot.plot_number,

        "booking_amount": float(booking.booking_amount),

        "advance": float(booking.advance_amount),

        "total_paid": float(total_paid),

        "remaining": float(remaining),

        "status": booking.status,

    })