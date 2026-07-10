from django import forms

from .models import Registration
from bookings.models import Booking


class RegistrationForm(forms.ModelForm):

    booking = forms.ModelChoiceField(
        queryset=Booking.objects.none(),
        empty_label="Select Fully Paid Booking",
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:

        model = Registration

        fields = [
            "booking",
            "registration_date",
            "registrar_office",
            "registration_number",
            "document_number",
            "sale_deed_number",
            "market_value",
            "stamp_duty",
            "registration_fee",
            "remarks",
            "sale_deed",
            "registration_copy",
            "ec_document",
            "tax_receipt",
            "other_document",
        ]

        widgets = {

            "registration_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "registrar_office": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "registration_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "document_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "sale_deed_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "market_value": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "stamp_duty": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "registration_fee": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "sale_deed": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "registration_copy": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "ec_document": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "tax_receipt": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "other_document": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Show only fully paid bookings that are not yet registered
        self.fields["booking"].queryset = Booking.objects.filter(
            status="fully_paid",
            registration__isnull=True
        )

        self.fields["booking"].label_from_instance = (
            lambda obj:
            f"{obj.booking_id} | "
            f"{obj.booked_client_name} | "
            f"{obj.project.project_name} | "
            f"Plot {obj.plot.plot_number}"
        )