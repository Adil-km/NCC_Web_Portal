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