from django import forms
from django.core.exceptions import ValidationError
from homepage.models import Homepage, WebsiteSection

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

class WebsiteSectionForm(forms.ModelForm):

    class Meta:
        model = WebsiteSection
        fields = [
            'section',
            'title',
            'description',
        ]

        labels = {
            'section': 'Section',
            'title': 'Title',
            'description': 'Description',
        }

        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),
        }
