from django.db import models
from django.core.validators import FileExtensionValidator

class Gallery(models.Model):

    # CATEGORY CHOICES
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('events', 'Events'),
        ('achievement', 'Achievement'),
        ('gallery', 'Gallery'),
    ]

    # VISIBILITY CHOICES
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=150)

    description = models.CharField(
        max_length=255,
        blank=True
    )

    content = models.TextField(
        blank=True
    )

    author = models.CharField(
        max_length=100,
        blank=True
    )

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='public'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    # User-selected date (event/news date)
    date = models.DateField()

    image = models.ImageField(
        upload_to='gallery/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        ]
    )

    # Automatically handled timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
