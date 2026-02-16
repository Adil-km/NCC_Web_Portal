from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Homepage(models.Model):
    CATEGORY_CHOICES = [
        ('slider', 'Slider'),
        ('about', 'About'),
        ('achievement', 'Achievement'),
        ('gallery', 'Gallery'),
    ]
    section = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    image = models.ImageField(
        upload_to='homepage/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.section
