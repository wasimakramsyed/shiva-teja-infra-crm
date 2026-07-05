from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name',
            'surname',
            'father_spouse_name',
            'mobile_number',
            'emergency_contact',
            'email',
            'address',
            'designation',
            'reporting_to',
            'joining_date',
            'status',
            'aadhaar',
            'pan',
            'passbook',
            'photo',
            'bank_account'
        ]

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'surname': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'father_spouse_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'mobile_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'emergency_contact': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
            'designation': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'reporting_to': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'joining_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'bank_account': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # File fields styling
        self.fields['aadhaar'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['pan'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['passbook'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['photo'].widget.attrs.update({
            'class': 'form-control'
        })

        hierarchy = [
            'SA',
            'SO',
            'ASM',
            'SM',
            'AGM',
            'GM',
            'DD',
            'DIR',
            'SD',
            'ED',
            'SED',
            'VP',
            'PRES',
            'MD',
            'CH'
        ]

        designation = None

        if self.data.get('designation'):
            designation = self.data.get('designation')
        elif self.instance.pk:
            designation = self.instance.designation

        if designation in hierarchy:
            current_index = hierarchy.index(designation)

            higher_designations = hierarchy[
                current_index + 1:
            ]

            self.fields[
                'reporting_to'
            ].queryset = Employee.objects.filter(
                designation__in=higher_designations
            )
        else:
            self.fields[
                'reporting_to'
            ].queryset = Employee.objects.none()