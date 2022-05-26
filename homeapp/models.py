from django.db import models

# Create your models here.

class Carausel(models.Model):
    image = models.ImageField(upload_to='picture/', null=True, blank=True)
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=100)

    def __str__(self):
        return self.title