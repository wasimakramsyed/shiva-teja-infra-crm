from django import forms
from .models import Lead
from employees.models import Employee
from teams.models import Team
from projects.models import Project


class LeadForm(forms.ModelForm):
    assigned_employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        empty_label="Select Employee",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    assigned_team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        empty_label="Select Team",
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        empty_label="Select Project",
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Lead
        fields = [
            'lead_name',
            'mobile_number',
            'email',
            'address',
            'source',
            'project',
            'assigned_employee',
            'assigned_team',
            'priority',
            'follow_up_date',
            'next_follow_up',
            'remarks',
            'status'
        ]

        widgets = {
            'lead_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'mobile_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),

            'source': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'priority': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'follow_up_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'next_follow_up': forms.DateInput(
                attrs={
                    'type': 'date',
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
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            'assigned_employee'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.first_name} "
                f"{obj.surname} "
                f"({obj.get_designation_display()})"
            )
        )

        self.fields[
            'assigned_team'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.team_name}"
            )
        )

        self.fields[
            'project'
        ].label_from_instance = (
            lambda obj: (
                f"{obj.project_name}"
            )
        )