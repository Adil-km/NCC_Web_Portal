from django import forms
from django.core.exceptions import ValidationError

from gallery.models import Gallery

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image','description']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = image.name.split('.')[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError(
                    "Only PNG and JPEG images are allowed."
                )
        return image