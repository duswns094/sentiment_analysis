from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Diary(models.Model): # DB Table for 설문조사 주제
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diaries')
    title = models.CharField(max_length=100) # 다이어리 제목
    content = models.TextField()
    image = models.ImageField(upload_to='diary/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True,null=False)
    real_date = models.DateField(null=False)
    emoji = models.ImageField(null=True, blank=True)
    positive = models.FloatField(null=True,blank=True)
    negative = models.FloatField(null=True,blank=True)
    neutral = models.FloatField(null=True,blank=True)
    advice = models.CharField(max_length = 200)

    def __str__(self):
        return self.title
