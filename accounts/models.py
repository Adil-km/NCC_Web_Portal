from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CADET = "CADET", "Cadet"
        FACULTY = "FACULTY", "Faculty"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CADET)
    
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
        related_name="tags"
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
