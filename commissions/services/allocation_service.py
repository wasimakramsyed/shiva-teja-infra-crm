from commissions.models import CommissionAllocation


class CommissionAllocationService:

    @staticmethod
    def create(
        commission,
        employee,
        percentage,
        gross_amount,
        tds_amount,
        net_amount,
    ):

        return CommissionAllocation.objects.create(
            commission=commission,
            employee=employee,
            percentage=percentage,
            gross_amount=gross_amount,
            tds_amount=tds_amount,
            net_amount=net_amount,
        )