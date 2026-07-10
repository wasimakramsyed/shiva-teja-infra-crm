from django import forms
from .models import Commission


class CommissionForm(forms.ModelForm):

    class Meta:

        model = Commission

        fields = [
            "remarks",
            "status",
        ]

        widgets = {

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }