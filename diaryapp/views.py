import re
from tokenization_kobert import KoBertTokenizer
import numpy as np
from django.conf import settings
import tensorflow as tf
import tensorflow_addons as tfa
import transformers
from transformers import TFBertModel
import sentencepiece as spm


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from django.views.generic import CreateView, ListView, DetailView, UpdateView

from diaryapp.decorators import diary_ownership_required
from diaryapp.forms import DiaryCreationForm
from diaryapp.models import Diary
from PIL import Image
from django.core.files.uploadedfile import UploadedFile


def prediction(sentence):
    # 2) Load the Bert-tokenizer
    tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')
    SEQ_LEN = 128 # 최대 token 개수 이상의 값으로 임의로 설정

    token_ids =[]
    token_masks =[]
    token_segments =[]


        # 특수문자 제거
    cleaned_sentence = re.sub("[^\s0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]", "", sentence) # [ whitespaces, 숫자, 영문 알파벳, 한글(+자모음) ]이 아닌 것을 공백으로 치환 (특수문자 제거)

    # Tokenizing / Tokens to sequence numbers / Padding
    encoded_dict = tokenizer.encode_plus(text=cleaned_sentence,
                                         padding='max_length',
                                         truncation = True,
                                         max_length=SEQ_LEN) # SEQ_LEN == 512

    token_ids.append(encoded_dict['input_ids']) # tokens_tensor
    token_masks.append(encoded_dict['attention_mask']) # masks_tensor
    token_segments.append(encoded_dict['token_type_ids']) # segments_tensor


    inputs = (np.array(token_ids), np.array(token_masks), np.array(token_segments))

    pred_model = settings.MODEL
    prediction = pred_model.predict(inputs)
    predicted_probability = np.round(np.max(prediction) * 100,
                                     2)  # ex) [[0.0125517 0.9874483, 0.0000000]]
    predicted_class = ['부정', '긍정', '중립'][
        np.argmax(prediction, axis=1)[0]]  # ex) ['부정', '긍정'][[1][0]] -> ['부정', '긍정'][1] -> '긍정'

    pred = "{}% 확률로 {} 문장입니다.".format(predicted_probability, predicted_class)

    return prediction

@method_decorator(login_required(login_url="/accounts/login/"), 'get')
@method_decorator(login_required(login_url="/accounts/login/"), 'post')
class DiaryCreateView(CreateView):
    model = Diary
    context_object_name = 'target_diary'
    form_class = DiaryCreationForm
    template_name = 'diaryapp/create.html'

    def form_valid(self, form):
        try:
            temp_diary = form.save(commit=False)
            temp_diary.writer = self.request.user
            pred = prediction(temp_diary.content)
            temp_diary.negative = np.round(pred[0][0],2)
            temp_diary.positive = np.round(pred[0][1],2)
            temp_diary.neutral = np.round(pred[0][2],2)
            predicted_class = ['부정', '긍정', '중립'][
                np.argmax(pred, axis=1)[0]]
            if predicted_class =='부정':
                temp_diary.color = '5C527F'
                temp_diary.emoji=UploadedFile(file=open("media/emoji/bad.png", 'rb'))
            elif predicted_class == '긍정':
                temp_diary.color='EF9F9F'
                temp_diary.emoji=UploadedFile(file=open("media/emoji/good.png", 'rb'))
            else:
                temp_diary.color='FFE3A9'
                temp_diary.emoji=UploadedFile(file=open("media/emoji/neutral2.png", 'rb'))
            temp_diary.save()
            return super().form_valid(form)
        except:
            print("실패")


    def get_success_url(self):
        return reverse('diaries:list')

@method_decorator(login_required(login_url="/accounts/login/"), 'get')
class DiaryListView(ListView):
    model = Diary
    context_object_name = 'diary_list'
    template_name = 'diaryapp/list.html'
    paginate_by = 21

    def get_queryset(self):  # 컨텍스트 오버라이딩
        return Diary.objects.filter(writer=self.request.user).order_by('-real_date')


@method_decorator(login_required(login_url="/accounts/login/"), 'get')
@method_decorator(diary_ownership_required, 'get')
class DiaryDetailView(DetailView):
    model = Diary
    context_object_name = 'target_diary'
    template_name = 'diaryapp/detail.html'


@method_decorator(diary_ownership_required, 'get')
@method_decorator(diary_ownership_required, 'post')
class DiaryUpdateView(UpdateView):
    model = Diary
    context_object_name = 'target_diary'
    form_class = DiaryCreationForm
    template_name = 'diaryapp/update.html'
    def form_valid(self, form):
        try:
            temp_diary = form.save(commit=False)
            pred = prediction(temp_diary.content)
            temp_diary.negative = np.round(pred[0][0],2)
            temp_diary.positive = np.round(pred[0][1],2)
            temp_diary.neutral = np.round(pred[0][2],2)
            predicted_class = ['부정', '긍정', '중립'][
                np.argmax(pred, axis=1)[0]]
            if predicted_class =='부정':
                temp_diary.color = '5C527F'
                temp_diary.emoji=UploadedFile(file=open("media/emoji/bad.png", 'rb'))
            elif predicted_class == '긍정':
                temp_diary.color='EF9F9F'
                temp_diary.emoji=UploadedFile(file=open("media/emoji/good.png", 'rb'))
            else:
                temp_diary.color='FFE3A9'
                temp_diary.emoji=UploadedFile(file=open("media/emoji/neutral2.png", 'rb'))
            temp_diary.save()
            return super().form_valid(form)
        except:
            print("실패")
    def get_success_url(self):
        return reverse('diaries:detail', kwargs={'pk':self.object.pk})

@method_decorator(login_required(login_url="/accounts/login/"), 'get')
class DiaryCalendarView(ListView):
    model = Diary
    context_object_name = 'diary_list'
    template_name = 'diaryapp/calendar.html'
    ordering = ['-created_at']
    paginate_by = 21

    def get_queryset(self):  # 컨텍스트 오버라이딩
        return Diary.objects.filter(writer=self.request.user)

