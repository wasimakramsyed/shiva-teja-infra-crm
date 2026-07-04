from django import forms
from .models import Team
from employees.models import Employee


class TeamForm(forms.ModelForm):
    team_head = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        empty_label="Select Team Head",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    members = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Team
        fields = [
            'team_name',
            'team_head',
            'members',
            'description',
            'status'
        ]

        widgets = {
            'team_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'description': forms.Textarea(
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

        # Team Head labels
        self.fields['team_head'].label_from_instance = (
            lambda obj: (
                f"{obj.first_name} "
                f"{obj.surname} "
                f"({obj.get_designation_display()})"
            )
        )

        # Members labels
        self.fields['members'].label_from_instance = (
            lambda obj: (
                f"{obj.first_name} "
                f"{obj.surname} "
                f"({obj.get_designation_display()})"
            )
        )