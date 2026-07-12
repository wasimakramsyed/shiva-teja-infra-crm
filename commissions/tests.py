from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from commissions.services.generator_service import CommissionGeneratorService


class CommissionGeneratorServiceTests(TestCase):
    def test_build_allocations_uses_percentage_inputs_for_all_employee_shares(self):
        allocations = CommissionGeneratorService.build_allocations(
            gross_commission=Decimal("120000.00"),
            tds_amount=Decimal("6000.00"),
            net_commission=Decimal("113500.00"),
            allocations=[
                {"employee": "emp-1", "percentage": Decimal("70.00")},
                {"employee": "emp-2", "percentage": Decimal("30.00")},
            ],
        )

        self.assertEqual(len(allocations), 2)
        self.assertEqual(allocations[0]["percentage"], Decimal("70.00"))
        self.assertEqual(allocations[0]["gross_share"], Decimal("84000.00"))
        self.assertEqual(allocations[0]["tds_share"], Decimal("4200.00"))
        self.assertEqual(allocations[0]["net_share"], Decimal("79450.00"))
        self.assertEqual(allocations[1]["net_share"], Decimal("34050.00"))

    def test_validate_allocations_requires_exactly_100_percent(self):
        with self.assertRaises(ValidationError):
            CommissionGeneratorService.validate_allocations(
                [Decimal("60.00"), Decimal("39.99")]
            )
