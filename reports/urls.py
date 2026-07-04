from django.urls import path
from .views import (
    reports_home,
    export_bookings_csv,
    export_payments_csv,
    export_bookings_pdf
)

urlpatterns = [
    path(
        'reports/',
        reports_home,
        name='reports_home'
    ),

    path(
        'reports/export/bookings/',
        export_bookings_csv,
        name='export_bookings_csv'
    ),

    path(
        'reports/export/payments/',
        export_payments_csv,
        name='export_payments_csv'
    ),

    path(
        'reports/export/bookings/pdf/',
        export_bookings_pdf,
        name='export_bookings_pdf'
    ),
]