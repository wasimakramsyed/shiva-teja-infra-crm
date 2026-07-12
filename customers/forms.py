from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [

            "customer_name",

            "mobile_number",

            "alternative_number",

            "email",

            "address",

            "aadhaar",

            "pan",

            "photo",

            "address_proof",

            "nominee_name",

            "relationship",

            "nominee_mobile",

        ]

        widgets = {

            "customer_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "mobile_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "alternative_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "nominee_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "relationship": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "nominee_mobile": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }