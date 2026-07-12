from django.db.models import Sum, Count
from commissions.models import CommissionRecord
from employees.models import Employee
from teams.models import Team
from projects.models import Project


class ReportService:

    @staticmethod
    def commission_summary(request):
        commissions = CommissionRecord.objects.select_related(
            "customer",
            "project",
            "booking",
            "request",
        )

        employee = request.GET.get("employee")
        customer = request.GET.get("customer")
        team = request.GET.get("team")
        project = request.GET.get("project")
        status = request.GET.get("status")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        if customer:
            commissions = commissions.filter(
                customer__customer_name__icontains=customer
            )

        if employee:
            commissions = commissions.filter(
                request__employee_id=employee
            )

        if team:
            commissions = commissions.filter(
                request__team_id=team
            )

        if project:
            commissions = commissions.filter(
                project_id=project
            )

        if status:
            commissions = commissions.filter(
                status=status
            )

        if from_date:
            commissions = commissions.filter(
                created_at__date__gte=from_date
            )

        if to_date:
            commissions = commissions.filter(
                created_at__date__lte=to_date
            )

        return {
            "generated": commissions.filter(status="generated").count(),
            "approved": commissions.filter(status="approved").count(),
            "paid": commissions.filter(status="paid").count(),
            "gross": commissions.aggregate(
                total=Sum("gross_commission")
            )["total"] or 0,
            "tds": commissions.aggregate(
                total=Sum("tds_amount")
            )["total"] or 0,
            "net": commissions.aggregate(
                total=Sum("net_commission")
            )["total"] or 0,
            "records": commissions.order_by("-created_at"),
            "employee_summary": commissions.values(
                "request__employee",
                "request__employee__employee_id",
                "request__employee__first_name",
                "request__employee__surname",
            ).annotate(
                gross=Sum("gross_commission"),
                tds=Sum("tds_amount"),
                net=Sum("net_commission"),
                total=Count("id"),
            ).order_by("-net"),
            "team_summary": commissions.values(
                "request__team",
                "request__team__team_name",
            ).annotate(
                gross=Sum("gross_commission"),
                tds=Sum("tds_amount"),
                net=Sum("net_commission"),
                total=Count("id"),
            ).order_by("-net"),
            "project_summary": commissions.values(
                "project",
                "project__project_name",
            ).annotate(
                gross=Sum("gross_commission"),
                tds=Sum("tds_amount"),
                net=Sum("net_commission"),
                total=Count("id"),
            ).order_by("-net"),
            "total": commissions.aggregate(
                total=Count("id")
            )["total"] or 0,
            "employees": Employee.objects.all(),
            "teams": Team.objects.all(),
            "projects": Project.objects.all(),
            "selected_employee": employee,
            "selected_team": team,
            "selected_project": project,
            "selected_status": status,
            "from_date": from_date,
            "to_date": to_date,
            "customer": customer,
        }