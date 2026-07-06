from django import forms
from .models import Payment
from bookings.models import Booking


class PaymentForm(forms.ModelForm):
    booking = forms.ModelChoiceField(
        queryset=Booking.objects.all(),
        empty_label="Select Booking",
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:
        model = Payment
        exclude = [
            'payment_id',
            'receipt_number'
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

            'receipt_upload': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        booking_id = kwargs.pop(
            'booking_id',
            None
        )

        super().__init__(*args, **kwargs)

        # Better booking dropdown display
        self.fields[
            'booking'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.booking_id} | "
                f"{obj.booked_client_name} | "
                f"{obj.project.project_name} | "
                f"{obj.plot.plot_number}"
            )
        )

        # Auto-select booking if opened from booking profile
        if booking_id:
            self.fields['booking'].initial = booking_id
            self.fields['booking'].widget.attrs[
                'readonly'
            ] = True