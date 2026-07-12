from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from commissions.models import CommissionRecord
from activities.activity_service import ActivityService as CRMActivityService

from .calculator import CommissionCalculator
from .allocation_service import CommissionAllocationService
from .timeline_service import CommissionTimelineService


class CommissionGeneratorService:

    @staticmethod
    def _quantize(value):
        return value.quantize(Decimal("0.01"))

    @staticmethod
    def validate_allocations(request, allocations):
        if not allocations:
            raise ValidationError("At least one employee allocation is required.")

        if request.employee:
            allowed_employees = [request.employee]
        elif request.team:
            allowed_employees = list(request.team.members.all())
        else:
            allowed_employees = []

        allowed_ids = {employee.id for employee in allowed_employees}
        seen_employees = set()
        total_percentage = Decimal("0.00")

        for allocation in allocations:
            employee = allocation["employee"]
            percentage = Decimal(str(allocation["percentage"]))

            if employee.id not in allowed_ids:
                raise ValidationError(
                    f"{employee} is not part of the assigned sales team."
                )

            if employee.status != "active":
                raise ValidationError(
                    f"{employee} must be Active before commission can be generated."
                )

            if employee.id in seen_employees:
                raise ValidationError(
                    f"{employee} cannot appear more than once in the allocation table."
                )

            if percentage < Decimal("0.00"):
                raise ValidationError(
                    f"Allocation percentage for {employee} cannot be negative."
                )

            if percentage > Decimal("100.00"):
                raise ValidationError(
                    f"Allocation percentage for {employee} cannot exceed 100%."
                )

            seen_employees.add(employee.id)
            total_percentage += percentage

        if total_percentage != Decimal("100.00"):
            raise ValidationError(
                "Total employee allocation must equal exactly 100%."
            )

    @staticmethod
    def build_allocations(
        request,
        gross_commission,
        tds_amount,
        net_commission,
        allocations,
    ):
        if not allocations:
            raise ValueError("No commission allocation found.")

        CommissionGeneratorService.validate_allocations(request, allocations)

        built_allocations = []

        for allocation in allocations:
            percentage = Decimal(str(allocation["percentage"]))
            gross_share = (gross_commission * percentage) / Decimal("100")
            tds_share = (tds_amount * percentage) / Decimal("100")
            net_share = (net_commission * percentage) / Decimal("100")

            built_allocations.append({
                "employee": allocation["employee"],
                "allocation_percentage": CommissionGeneratorService._quantize(percentage),
                "gross_share": CommissionGeneratorService._quantize(gross_share),
                "tds_share": CommissionGeneratorService._quantize(tds_share),
                "net_share": CommissionGeneratorService._quantize(net_share),
            })

        return built_allocations

    @staticmethod
    @transaction.atomic
    def generate(
        request,
        commission_percentage,
        tds_percentage,
        allocations,
        generated_by,
        other_deduction=0,
        remarks=""
    ):

        if not allocations:
            raise ValueError("No commission allocation found.")

        if request.status != "ready":
            raise ValueError(
                "Commission has already been processed."
            )

        if hasattr(request, "record"):
            raise ValueError(
                "Commission Record already exists."
            )

        calculation = CommissionCalculator.calculate(
            sale_amount=request.sale_amount,
            commission_percentage=commission_percentage,
            tds_percentage=tds_percentage,
            other_deduction=other_deduction,
        )

        built_allocations = CommissionGeneratorService.build_allocations(
            request=request,
            gross_commission=calculation["gross_commission"],
            tds_amount=calculation["tds_amount"],
            net_commission=calculation["net_commission"],
            allocations=allocations,
        )

        commission = CommissionRecord.objects.create(
            request=request,
            booking=request.booking,
            customer=request.customer,
            customer_property=request.customer_property,
            project=request.project,
            plot=request.plot,
            sale_amount=request.sale_amount,
            commission_percentage=commission_percentage,
            gross_commission=calculation["gross_commission"],
            tds_percentage=tds_percentage,
            tds_amount=calculation["tds_amount"],
            other_deduction=other_deduction,
            net_commission=calculation["net_commission"],
            generated_by=generated_by,
            remarks=remarks,
        )

        CRMActivityService.create_activity(
            customer=request.customer,
            booking=request.booking,
            commission=commission,
            activity_type="commission",
            title="Commission Generated",
            description=(
                f"Commission {commission.record_id} generated for "
                f"{request.customer.customer_name}."
            ),
            created_by=generated_by,
            icon="fas fa-coins",
            color="orange",
            is_system_generated=True,
        )

        for allocation in built_allocations:
            CommissionAllocationService.create(
                commission=commission,
                employee=allocation["employee"],
                percentage=allocation["allocation_percentage"],
                gross_amount=allocation["gross_share"],
                tds_amount=allocation["tds_share"],
                net_amount=allocation["net_share"],
            )

        CommissionTimelineService.create(
            commission=commission,
            activity="Commission Generated",
            created_by=generated_by,
            remarks=remarks,
        )

        request.status = "generated"
        request.generated_by = generated_by
        request.generated_at = timezone.now()
        request.save()

        return commission