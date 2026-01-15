from django import forms
from django.core.exceptions import ValidationError
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'activity_type', 'start_date', 'end_date', 'location']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            # ... other widgets ...
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError("End date cannot be before start date.")
            
            # Optional: Warning if activity is too long (e.g., > 30 days)
            diff = end_date - start_date
            if diff.days > 30:
                raise ValidationError(f"Activity duration is {diff.days} days. Is this correct? Please check the dates.")

        return cleaned_data