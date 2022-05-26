from django.contrib import admin

# Register your models here.
from diaryapp.models import Diary


class DiaryAdmin(admin.ModelAdmin):
    list_display = ['real_date', 'writer', 'created_at']
    list_display_links = ['real_date']

admin.site.register(Diary, DiaryAdmin)