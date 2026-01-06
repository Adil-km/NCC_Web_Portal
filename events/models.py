from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

class NewsEvent(models.Model):  # Renamed to singular (Django convention)
    
    # Using TextChoices for better readability and type safety
    class Category(models.TextChoices):
        NEWS = 'news', _('News')
        EVENTS = 'events', _('Events')
        ACHIEVEMENT = 'achievement', _('Achievement')

    class Visibility(models.TextChoices):
        PUBLIC = 'public', _('Public')
        PRIVATE = 'private', _('Private')

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True) # Added for SEO-friendly URLs
    content = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PUBLIC
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.NEWS
    )

    # Specific date for the event/news item
    event_date = models.DateField() 

    image = models.ImageField(
        upload_to='news_events/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])],
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("News and Event")
        verbose_name_plural = _("News and Events")
        ordering = ['-event_date', '-created_at']

    def __str__(self):
        return f"{self.get_category_display()}: {self.title}"