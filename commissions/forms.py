from django import forms
from .models import Commission
from employees.models import Employee
from payments.models import Payment


class CommissionForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        empty_label="Select Employee",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    payment = forms.ModelChoiceField(
        queryset=Payment.objects.all(),
        empty_label="Select Payment",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Commission
        fields = [
            'employee',
            'payment',
            'commission_percentage',
            'tds',
            'remarks',
            'status',
            'paid_date'
        ]

        widgets = {
            'commission_percentage': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'tds': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'paid_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'employee'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.employee_id} - "
                f"{obj.first_name} "
                f"{obj.surname} "
                f"({obj.designation})"
            )
        )

        self.fields[
            'payment'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.payment_id} - "
                f"{obj.booking.booked_client_name}"
            )
        )