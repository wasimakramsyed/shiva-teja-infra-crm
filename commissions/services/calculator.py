from decimal import Decimal


class CommissionCalculator:

    @staticmethod
    def calculate(
        sale_amount,
        commission_percentage,
        tds_percentage,
        other_deduction=0
    ):

        sale_amount = Decimal(sale_amount)
        commission_percentage = Decimal(commission_percentage)
        tds_percentage = Decimal(tds_percentage)
        other_deduction = Decimal(other_deduction)

        gross_commission = (
            sale_amount * commission_percentage
        ) / Decimal("100")

        tds_amount = (
            gross_commission * tds_percentage
        ) / Decimal("100")

        net_commission = (
            gross_commission
            - tds_amount
            - other_deduction
        )

        return {
            "gross_commission": gross_commission,
            "tds_amount": tds_amount,
            "net_commission": net_commission,
        }