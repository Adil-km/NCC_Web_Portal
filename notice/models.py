from django.db import models

class Notice(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.name
