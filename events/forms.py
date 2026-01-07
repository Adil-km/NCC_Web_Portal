from django import forms
from django.core.exceptions import ValidationError
from .models import NewsEvent

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


class NewsEventForm(forms.ModelForm):

    class Meta:
        model = NewsEvent
        fields = [
            'image',
            'title',
            'content',
            'author',
            'visibility',
            'category',
            'date',
        ]

        labels = {
            'image': 'Image (optional)',
            'title': 'Title',
            'content': 'Content (optional)',
            'author': 'Author (optional)',
            'visibility': 'Visibility',
            'category': 'Category',
            'date': 'Event Date',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title'
            }),
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write news or event details (optional)'
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
