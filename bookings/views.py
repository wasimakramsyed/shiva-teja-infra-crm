from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from bookings.services.booking_service import BookingService
from django.http import HttpResponse
from reportlab.pdfgen import canvas
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
# ==========================================================
# Booking List
# ==========================================================
@role_required(['admin', 'manager', 'sales'])
def booking_list(request):

    query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    project_filter = request.GET.get("project", "").strip()

    bookings = Booking.objects.select_related(
        "project",
        "plot",
        "lead",
        "assigned_employee",
        "assigned_team",
    )

    # ----------------------------------
    # Project Filter
    # ----------------------------------

    if project_filter:

        bookings = bookings.filter(
            project_id=project_filter
        )

    # ----------------------------------
    # Search
    # ----------------------------------

    if query:

        bookings = bookings.filter(

            Q(booking_id__icontains=query) |

            Q(booked_client_name__icontains=query) |

            Q(mobile_number__icontains=query) |

            Q(project__project_name__icontains=query) |

            Q(plot__plot_number__icontains=query) |

            Q(assigned_employee__first_name__icontains=query) |

            Q(assigned_employee__surname__icontains=query) |

            Q(assigned_team__team_name__icontains=query)

        ).distinct()

    # ----------------------------------
    # Status Filter
    # ----------------------------------

    if status_filter:

        bookings = bookings.filter(
            status=status_filter
        )

    # ----------------------------------
    # Load Projects for Dropdown
    # ----------------------------------

    from projects.models import Project

    projects = Project.objects.order_by(
        "project_name"
    )

    return render(

        request,

        "bookings/booking_list.html",

        {

            "bookings": bookings,

            "projects": projects,

            "query": query,

            "status_filter": status_filter,

            "project_filter": project_filter,

        }

    )


# ==========================================================
# Create Booking
# ==========================================================
@role_required(['sales', 'admin', 'manager'])
def create_booking(request):

    form = BookingForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":

        if form.is_valid():

            try:

                booking = BookingService.create_booking(
                    form=form,
                    user=request.user
                )

                messages.success(
                    request,
                    f"Booking {booking.booking_id} created successfully."
                )

                return redirect(
                    "booking_profile",
                    booking_id=booking.id
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

    lead_id = request.GET.get("lead")

    if lead_id:

        try:

            lead = Lead.objects.get(id=lead_id)

            form.initial["lead"] = lead
            form.initial["booked_client_name"] = lead.lead_name
            form.initial["mobile_number"] = lead.mobile_number

        except Lead.DoesNotExist:
            pass

    return render(
        request,
        "bookings/create_booking.html",
        {
            "form": form
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
            'pending': pending,
            'activities': booking.activities.all()
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

    project_id = request.GET.get("project_id")

    print("=" * 60)
    print("PROJECT ID RECEIVED:", project_id)

    plots = Plot.objects.filter(
        project_id=project_id,
        status="available"
    )

    print("AVAILABLE PLOTS:", plots.count())

    for plot in plots:
        print(
            f"ID={plot.id}, "
            f"Plot={plot.plot_number}, "
            f"Status={plot.status}"
        )

    return JsonResponse(
        list(
            plots.values(
                "id",
                "plot_number"
            )
        ),
        safe=False
    )
# ==========================================================
# Print Booking
# ==========================================================
@role_required(['admin', 'manager', 'sales'])
def print_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    payments = Payment.objects.filter(
        booking=booking
    )

    total_paid = booking.advance_amount + sum(
        payment.amount
        for payment in payments
    )

    pending = booking.booking_amount - total_paid

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; filename="{booking.booking_id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setTitle("Booking Confirmation")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        170,
        800,
        "SHIVA TEJA INFRA"
    )

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(
        180,
        775,
        "Booking Confirmation"
    )

    pdf.setFont("Helvetica", 11)

    y = 735

    details = [
        ("Booking ID", booking.booking_id),
        ("Booking Date", str(booking.booking_date)),
        ("Customer", booking.booked_client_name),
        ("Mobile", booking.mobile_number),
        ("Project", booking.project.project_name),
        ("Plot", booking.plot.plot_number),
        ("Booking Amount", f"₹ {booking.booking_amount}"),
        ("Advance Paid", f"₹ {booking.advance_amount}"),
        ("Total Paid", f"₹ {total_paid}"),
        ("Pending", f"₹ {pending}"),
        ("Status", booking.status),
    ]

    for label, value in details:

        pdf.drawString(
            60,
            y,
            f"{label}:"
        )

        pdf.drawString(
            220,
            y,
            str(value)
        )

        y -= 25

    pdf.line(
        60,
        120,
        220,
        120
    )

    pdf.drawString(
        60,
        100,
        "Authorized Signature"
    )

    pdf.save()

    return response