from django.db import models
from django.core.validators import FileExtensionValidator

class Homepage(models.Model):
    CATEGORY_CHOICES = [
        ('slider', 'Slider'),
        ('about', 'About'),
        ('achievement', 'Achievement'),
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

    def save(self, *args, **kwargs):
        if self.section == 'about':
            existing = Homepage.objects.filter(section='about').first()
            if existing and not self.pk:
                existing.image = self.image
                existing.save()
                return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.section
