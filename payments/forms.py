from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'payment_id',
            'booking',
            'payment_date',
            'amount',
            'payment_mode',
            'receipt_number',
            'status',
            'remarks'
        ]