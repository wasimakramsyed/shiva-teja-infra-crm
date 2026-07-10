from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from employees.models import Employee
from teams.models import Team
from projects.models import Project, Plot
from leads.models import Lead
from bookings.models import Booking
from customers.models import Customer
from payments.models import Payment
from registrations.models import Registration
from commissions.models import Commission


class DashboardService:

    @staticmethod
    def get_dashboard_data():

        total_revenue = (
            Payment.objects.aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        pending_collection = (
            Booking.objects.aggregate(
                total=Sum("pending_amount")
            )["total"] or 0
        )
        # ==========================================
# Monthly Revenue Chart
# ==========================================

        monthly_revenue = (
            Payment.objects
            .annotate(month=TruncMonth("payment_date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        chart_labels = []
        chart_values = []

        for item in monthly_revenue:
            chart_labels.append(item["month"].strftime("%b"))
            chart_values.append(float(item["total"]))

        return {

            # Employees
            "total_employees":
                Employee.objects.count(),

            "total_teams":
                Team.objects.count(),

            # Projects
            "total_projects":
                Project.objects.count(),

            "total_plots":
                Plot.objects.count(),

            "available_plots":
                Plot.objects.filter(
                    status="available"
                ).count(),

            "booked_plots":
                Plot.objects.filter(
                    status="booked"
                ).count(),

            "sold_plots":
                Plot.objects.filter(
                    status="sold"
                ).count(),

            # Leads
            "total_leads":
                Lead.objects.count(),

            # Bookings
            "total_bookings":
                Booking.objects.count(),

            # Customers
            "total_customers":
                Customer.objects.count(),

            # Payments
            "total_payments":
                Payment.objects.count(),

            "total_revenue":
                total_revenue,

            "pending_collection":
                pending_collection,

            # Registrations
            "total_registrations":
                Registration.objects.count(),

            # Commission
            "generated_commissions":
                Commission.objects.filter(
                    status="generated"
                ).count(),

            "approved_commissions":
                Commission.objects.filter(
                    status="approved"
                ).count(),

            "paid_commissions":
                Commission.objects.filter(
                    status="paid"
                ).count(),

            # Recent Data
            "recent_bookings":
                Booking.objects.order_by(
                    "-id"
                )[:5],

            "recent_payments":
                Payment.objects.order_by(
                    "-payment_date"
                )[:5],

            "recent_customers":
                Customer.objects.order_by(
                    "-id"
                )[:5],

            "chart_labels": chart_labels,

            "chart_values": chart_values,
        }