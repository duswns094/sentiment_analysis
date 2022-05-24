from django.contrib import admin

# Register your models here.
from diaryapp.models import Diary


class DiaryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'created_at']
    list_display_links = ['title']

admin.site.register(Diary, DiaryAdmin)