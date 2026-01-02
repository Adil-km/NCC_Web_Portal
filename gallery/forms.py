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
            'description',
            'content',
            'author',
            'visibility',
            'category',
            'date',
        ]

        labels = {
            'image': 'Image',
            'title': 'Title',
            'description': 'Description (optional)',
            'content': 'Content (optional)',
            'author': 'Author (optional)',
            'visibility': 'Visibility',
            'category': 'Category',
            'date': 'Date',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Short description (optional)'
            }),
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Detailed content (optional)'
            }),
            'author': forms.TextInput(attrs={
                'placeholder': 'Author name (optional)'
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
            ext = image.name.split('.')[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError(
                    "Only PNG and JPEG images are allowed."
                )

        return image
