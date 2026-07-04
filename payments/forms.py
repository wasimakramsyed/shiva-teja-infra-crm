from django import forms
from .models import Payment
from bookings.models import Booking


class PaymentForm(forms.ModelForm):
    booking = forms.ModelChoiceField(
        queryset=Booking.objects.all(),
        empty_label="Select Booking",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Payment
        fields = [
            'booking',
            'payment_date',
            'amount',
            'payment_mode',
            'transaction_id',
            'receipt_number',
            'receipt_upload',
            'remarks',
            'status'
        ]

        widgets = {
            'payment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'payment_mode': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'transaction_id': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'receipt_number': forms.TextInput(
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