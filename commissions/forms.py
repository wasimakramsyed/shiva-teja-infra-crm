from django import forms
 

# ==============================
# Legacy Commission Form
# ==============================

 


# ==============================
# New Commission Generation Form
# ==============================

class CommissionGenerationForm(forms.Form):

    commission_percentage = forms.DecimalField(
        label="Commission %",
        max_digits=5,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Enter Commission %",
            }
        ),
    )

    tds_percentage = forms.DecimalField(
        label="TDS %",
        max_digits=5,
        decimal_places=2,
        initial=10,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
            }
        ),
    )

    other_deduction = forms.DecimalField(
        label="Other Deduction",
        required=False,
        initial=0,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Optional Remarks",
            }
        ),
    )