from django.forms import ModelForm
from django import forms
from datetime import datetime
from diaryapp.models import Diary

class DiaryCreationForm(ModelForm):

    class Meta:
        model = Diary
        fields = ['real_date','content','image']
        widgets = {
            'real_date': forms.DateInput(attrs={
                'format': '%Y-%m-%d',
                'class': "form-control",
                'type': 'date',
            }),
            'content': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder': '내용을 입력해주세요'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

