from django.forms import ModelForm
from django import forms
from datetime import datetime
from diaryapp.models import Diary

class DiaryCreationForm(ModelForm):

    class Meta:
        model = Diary
        fields = ['title','content','real_date','image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': '제목을 입력해주세요'
            }),
            'content': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder': '내용을 입력해주세요'
            }),
            'real_date': forms.DateInput(attrs={
                'format' : '%Y-%m-%d',
                'class': "form-control",
                'type': 'date',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

