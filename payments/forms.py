from django import forms
from .models import Payment
from bookings.models import Booking


class PaymentForm(forms.ModelForm):

    booking = forms.ModelChoiceField(
        queryset=Booking.objects.filter(
            pending_amount__gt=0
        ).exclude(
            status="cancelled"
        ).select_related(
            "project",
            "plot"
        ),
        empty_label="Select Booking",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:

        model = Payment

        fields = [
            "booking",
            "payment_date",
            "amount",
            "payment_mode",
            "remarks",
        ]

        widgets = {

            "payment_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Payment Amount"
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Remarks (Optional)"
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        booking_id = kwargs.pop("booking_id", None)

        super().__init__(*args, **kwargs)

        self.fields["booking"].label_from_instance = (
            lambda obj:
            f"{obj.booking_id} | "
            f"{obj.booked_client_name} | "
            f"{obj.project.project_name} | "
            f"Plot {obj.plot.plot_number}"
        )

        self.fields["payment_mode"].choices = Payment.PAYMENT_MODE_CHOICES

        self.fields["booking"].label = "Booking"
        self.fields["payment_date"].label = "Payment Date"
        self.fields["amount"].label = "Payment Amount"
        self.fields["payment_mode"].label = "Payment Mode"
        self.fields["remarks"].label = "Remarks"

        if booking_id:

            self.fields["booking"].queryset = Booking.objects.filter(
                id=booking_id
            )

            self.fields["booking"].initial = booking_id

            self.fields["booking"].disabled = True