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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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