from django.urls import path

from .views import (
    reports_home,
    booking_report,
    payment_report,
    registration_report,
    commission_report,
    customer_report,
    employee_report,
    project_report,
    export_bookings_csv,
    export_payments_csv,
    export_bookings_pdf,
    export_commission_excel,
    export_commission_pdf,
)

urlpatterns = [

    path(
        "reports/",
        reports_home,
        name="reports_home",
    ),

    path(
        "reports/bookings/",
        booking_report,
        name="booking_report",
    ),

    path(
        "reports/payments/",
        payment_report,
        name="payment_report",
    ),

    path(
        "reports/registrations/",
        registration_report,
        name="registration_report",
    ),

    path(
        "reports/commissions/",
        commission_report,
        name="commission_report",
    ),

    path(
        "reports/customers/",
        customer_report,
        name="customer_report",
    ),

    path(
        "reports/employees/",
        employee_report,
        name="employee_report",
    ),

    path(
        "reports/projects/",
        project_report,
        name="project_report",
    ),

    path(
        "reports/export/bookings/",
        export_bookings_csv,
        name="export_bookings_csv",
    ),

    path(
        "reports/export/payments/",
        export_payments_csv,
        name="export_payments_csv",
    ),

    path(
        "reports/export/bookings/pdf/",
        export_bookings_pdf,
        name="export_bookings_pdf",
    ),

    path(
        "reports/export/commissions/excel/",
        export_commission_excel,
        name="export_commission_excel",
    ),

    path(
        "reports/export/commissions/pdf/",
        export_commission_pdf,
        name="export_commission_pdf",
    ),
]