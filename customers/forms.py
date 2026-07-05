from django import forms
from .models import Customer
from bookings.models import Booking


class CustomerForm(forms.ModelForm):
    booking = forms.ModelChoiceField(
        queryset=Booking.objects.filter(
            status='fully_paid'
        ),
        empty_label="Select Booking",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Customer
        fields = [
            'booking',
            'customer_name',
            'mobile_number',
            'alternative_number',
            'email',
            'address',
            'aadhaar',
            'pan',
            'photo',
            'address_proof',
            'nominee_name',
            'relationship',
            'nominee_mobile',
            'registration_status',
            'registration_date',
            'ownership_status'
        ]

        widgets = {
            'customer_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'mobile_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'alternative_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'nominee_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'relationship': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'nominee_mobile': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'registration_status': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'registration_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'ownership_status': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'booking'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.booking_id} - "
                f"{obj.booked_client_name}"
            )
        )