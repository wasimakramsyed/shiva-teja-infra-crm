from django import forms

from .models import Booking
from projects.models import Plot
from employees.models import Employee
from teams.models import Team


class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking

        fields = [
            "booking_date",
            "lead",
            "booking_source",
            "assigned_employee",
            "assigned_team",
            "project",
            "plot",
            "booked_client_name",
            "mobile_number",
            "booking_amount",
            "advance_amount",
            "payment_mode",
            "reference_number",
            "booking_remarks",
            "special_instructions",
            "booking_form",
            "customer_photo",
            "aadhaar",
            "pan",
        ]

        widgets = {

            "booking_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "lead": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "booking_source": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "assigned_employee": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "assigned_team": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "project": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "plot": forms.Select(
    attrs={
        "class": "form-select no-tom-select"
    }
),
            "booked_client_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Customer Name"
                }
            ),

            "mobile_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mobile Number"
                }
            ),

            "booking_amount": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "advance_amount": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "reference_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Reference Number (Optional)"
                }
            ),

            "booking_remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "special_instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "booking_form": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "customer_photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "aadhaar": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "pan": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # ------------------------
        # Labels
        # ------------------------

        self.fields["booking_amount"].label = "Total Plot Price"
        self.fields["advance_amount"].label = "Booking Advance"

        if not self.instance.pk:
            self.fields["advance_amount"].initial = None

        # ------------------------
        # Optional Files
        # ------------------------

        for field in [
            "booking_form",
            "customer_photo",
            "aadhaar",
            "pan",
        ]:
            self.fields[field].required = False

        # ------------------------
        # Employee & Team
        # ------------------------

        self.fields["assigned_employee"].queryset = Employee.objects.filter(
            status="active"
        ).order_by("first_name")

        self.fields["assigned_team"].queryset = Team.objects.filter(
            status="active"
        ).order_by("team_name")

        # ------------------------
        # Plot Loading
        # ------------------------

        self.fields["plot"].queryset = Plot.objects.none()

        if self.data.get("project"):

            try:

                project_id = int(
                    self.data.get("project")
                )

                self.fields["plot"].queryset = Plot.objects.filter(
                    project_id=project_id,
                    status="available"
                ).order_by("plot_number")

            except (ValueError, TypeError):
                pass

        elif self.instance.pk:

            self.fields["plot"].queryset = Plot.objects.filter(
                project=self.instance.project
            ).order_by("plot_number")

    def clean(self):

        cleaned_data = super().clean()

        lead = cleaned_data.get("lead")

        employee = cleaned_data.get("assigned_employee")
        team = cleaned_data.get("assigned_team")

        # Direct Booking

        if not lead:

            if not employee:
                self.add_error(
                    "assigned_employee",
                    "Please select an employee."
                )

            if not team:
                self.add_error(
                    "assigned_team",
                    "Please select a team."
                )

        return cleaned_data