from django import forms
from django.core.exceptions import ValidationError
from gallery.models import Gallery

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = [
            'image',
            'title',
            'visibility',
            'category',
            'date',
        ]

        labels = {
            'image': 'Image',
            'title': 'Title',
            'visibility': 'Visibility',
            'category': 'Category',
            'date': 'Date',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title'
            }),
            'visibility': forms.RadioSelect(),
            'category': forms.Select(),
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            ext = image.name.rsplit('.', 1)[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError(
                    "Only PNG, JPG, and JPEG files are allowed."
                )

        return image
