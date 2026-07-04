from django import forms
from .models import Project, Plot


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_name',
            'location',
            'description',
            'total_plots',
            'project_value',
            'status'
        ]

        widgets = {
            'project_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'location': forms.TextInput(
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

            'total_plots': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'project_value': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        fields = [
            'project',
            'plot_number',
            'plot_size',
            'facing',
            'status'
        ]

        widgets = {
            'project': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'plot_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'plot_size': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'facing': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }