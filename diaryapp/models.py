from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Diary(models.Model): # DB Table for 설문조사 주제
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diaries')
    content = models.TextField()
    image = models.ImageField(upload_to='diary/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True,null=False)
    real_date = models.DateField(null=False)
    emoji = models.ImageField(upload_to='emoji/',null=True, blank=True)
    color = ColorField(null=True,blank=True)
    positive = models.FloatField(null=True,blank=True)
    negative = models.FloatField(null=True,blank=True)
    neutral = models.FloatField(null=True,blank=True)
    advice = models.CharField(max_length = 200,null=True,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['writer','real_date'],
                name="unique_diary"
            )
        ]
    def __str__(self):
        return str(self.real_date)+"_"+str(self.writer)
