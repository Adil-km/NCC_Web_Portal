from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CADET = "CADET", "Cadet"
        FACULTY = "FACULTY", "Faculty"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CADET)
    is_higher_faculty = models.BooleanField(default=False)
    
    assigned_faculty = models.ForeignKey(
            'self', 
            null=True, 
            blank=True, 
            on_delete=models.SET_NULL,
            related_name='assigned_cadets',
            limit_choices_to={'role': 'FACULTY'},
            help_text="Designate the Faculty advisor for this Cadet."
    )

class UserTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserTagAssignment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tags"   # IMPORTANT
    )
    tag = models.ForeignKey(
        UserTag,
        on_delete=models.CASCADE,
        related_name="users"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tag')
        indexes = [
            models.Index(fields=['user', 'tag']),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.tag.code}"
