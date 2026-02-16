from django import forms
from django.core.exceptions import ValidationError
from homepage.models import Homepage

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


class UploadHomePageForm(forms.ModelForm):

    class Meta:
        model = Homepage
        fields = [
            'section',
            'image',
        ]

        labels = {
            'image': 'Image',
            'section': 'Section',
        }

        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            ext = image.name.rsplit('.', 1)[-1].lower()
            if ext not in ['png', 'jpg', 'jpeg']:
                raise ValidationError(
                    "Only PNG, JPG, and JPEG files are allowed."
                )

        return image

