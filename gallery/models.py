from django.db import models
from django.core.validators import FileExtensionValidator

class Gallery(models.Model):
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='gallery/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        ]
    )