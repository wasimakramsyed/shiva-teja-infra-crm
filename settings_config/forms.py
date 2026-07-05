from django import forms
from .models import CRMSettings


class CRMSettingsForm(forms.ModelForm):
    class Meta:
        model = CRMSettings
        fields = [
            'tds_percentage',
            'gst_percentage',
            'default_commission_percentage'
        ]

        widgets = {
            'tds_percentage': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'gst_percentage': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'default_commission_percentage': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }