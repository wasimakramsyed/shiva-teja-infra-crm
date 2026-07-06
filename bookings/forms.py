from django import forms
from .models import Booking
from projects.models import Plot


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'booking_date',
            'lead',
            'project',
            'plot',
            'booked_client_name',
            'mobile_number',
            'booking_amount',
            'advance_amount',
            'payment_mode',
            'reference_number',
            'booking_remarks',
            'special_instructions',
            'booking_form',
            'customer_photo',
            'aadhaar',
            'pan'
        ]

        widgets = {
            'lead': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'booking_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'booked_client_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'mobile_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'project': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'plot': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'booking_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'advance_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'payment_mode': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'reference_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'booking_remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'special_instructions': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'booking_form': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'customer_photo': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'aadhaar': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'pan': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Better Labels
        self.fields['booking_amount'].label = "Total Plot Price"
        self.fields['advance_amount'].label = "Booking Advance"

        # Optional Documents
        for field in [
            'booking_form',
            'customer_photo',
            'aadhaar',
            'pan'
        ]:
            self.fields[field].required = False

        # No plots initially
        self.fields['plot'].queryset = Plot.objects.none()

        # Load plots after selecting project
        if self.data.get('project'):

            try:

                project_id = int(
                    self.data.get('project')
                )

                self.fields['plot'].queryset = Plot.objects.filter(
                    project_id=project_id,
                    status='available'
                ).order_by('plot_number')

            except (ValueError, TypeError):
                pass

        # Editing existing booking
        elif self.instance.pk:

            self.fields['plot'].queryset = Plot.objects.filter(
                project=self.instance.project
            ).order_by('plot_number')