from django.shortcuts import render
from django.http import HttpResponse
import csv
from reportlab.platypus import SimpleDocTemplate, Table

from payments.models import Payment
from commissions.models import Commission
from bookings.models import Booking
from projects.models import Plot
from accounts.decorators import role_required


@role_required(['admin', 'manager'])
def reports_home(request):
    context = {
        'total_sales': Booking.objects.count(),

        'total_revenue': sum(
            payment.amount
            for payment in Payment.objects.all()
        ),

        'pending_commissions': Commission.objects.filter(
            status='pending'
        ).count(),

        'booked_plots': Plot.objects.filter(
            status='booked'
        ).count(),

        'registered_plots': Plot.objects.filter(
            status='registered'
        ).count(),
    }

    return render(
        request,
        'reports/home.html',
        context
    )


# EXPORT BOOKINGS CSV
@role_required(['admin', 'manager'])
def export_bookings_csv(request):
    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="bookings.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Booking ID',
        'Customer Name',
        'Project',
        'Plot',
        'Amount',
        'Status'
    ])

    bookings = Booking.objects.all()

    for booking in bookings:
        writer.writerow([
            booking.booking_id,
            booking.customer.customer_name,
            booking.project.project_name,
            booking.plot.plot_number,
            booking.booking_amount,
            booking.status
        ])

    return response


# EXPORT PAYMENTS CSV
@role_required(['admin', 'manager'])
def export_payments_csv(request):
    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Payment ID',
        'Booking ID',
        'Amount',
        'Payment Mode',
        'Status',
        'Payment Date'
    ])

    payments = Payment.objects.all()

    for payment in payments:
        writer.writerow([
            payment.payment_id,
            payment.booking.booking_id,
            payment.amount,
            payment.payment_mode,
            payment.status,
            payment.payment_date
        ])

    return response


# EXPORT BOOKINGS PDF
@role_required(['admin', 'manager'])
def export_bookings_pdf(request):
    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="bookings.pdf"'

    doc = SimpleDocTemplate(response)

    data = [[
        'Booking ID',
        'Customer',
        'Project',
        'Plot',
        'Amount',
        'Status'
    ]]

    bookings = Booking.objects.all()

    for booking in bookings:
        data.append([
            booking.booking_id,
            booking.customer.customer_name,
            booking.project.project_name,
            booking.plot.plot_number,
            str(booking.booking_amount),
            booking.status
        ])

    table = Table(data)

    elements = [table]
    doc.build(elements)

    return response