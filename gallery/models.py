from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class Gallery(models.Model):

    # CATEGORY CHOICES
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('boys', 'NCC Army Boys'),
        ('girls', 'NCC Army Girls'),
        ('naval', 'NCC Naval'),
    ]

    # VISIBILITY CHOICES
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=150)

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='public'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )

    date = models.DateField(default=timezone.now)

    image = models.ImageField(
        upload_to='gallery/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
