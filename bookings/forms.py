from django import forms
from .models import Booking
from leads.models import Lead
from projects.models import Project, Plot


class BookingForm(forms.ModelForm):
    lead = forms.ModelChoiceField(
        queryset=Lead.objects.all(),
        empty_label="Select Lead",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        empty_label="Select Project",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    plot = forms.ModelChoiceField(
        queryset=Plot.objects.filter(
            status='available'
        ),
        empty_label="Select Plot",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Booking
        fields = [
            'booking_date',
            'lead',
            'project',
            'plot',
            'booked_client_name',
            'mobile_number',
            'booking_amount',
            'advance_amount',
            'payment_mode',
            'reference_number',
            'booking_remarks',
            'special_instructions',
            'booking_form',
            'customer_photo',
            'aadhaar',
            'pan',
            'status'
        ]

        widgets = {
            'booking_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'booked_client_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'mobile_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'booking_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'advance_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'payment_mode': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'reference_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'booking_remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'special_instructions': forms.Textarea(
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'lead'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.lead_name} "
                f"({obj.mobile_number})"
            )
        )

        self.fields[
            'project'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.project_name}"
            )
        )

        self.fields[
            'plot'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.plot_number} "
                f"- {obj.plot_size}"
            )
        )