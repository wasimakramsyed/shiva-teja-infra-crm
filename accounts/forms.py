from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(

        label="",

        widget=forms.TextInput(

            attrs={

                "class": "form-control form-control-lg",

                "placeholder": "Username or Mobile Number",

                "autocomplete": "username",

            }

        )

    )

    password = forms.CharField(

        label="",

        widget=forms.PasswordInput(

            attrs={

                "class": "form-control form-control-lg",

                "placeholder": "Password",

                "id": "password",

                "autocomplete": "current-password",

            }

        )

    )

    remember_me = forms.BooleanField(

        required=False

    )