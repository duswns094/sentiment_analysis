from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from diaryapp.decorators import diary_ownership_required
from diaryapp.forms import DiaryCreationForm
from diaryapp.models import Diary
from PIL import Image

#for prediction
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
import pandas as pd
import numpy as np
from . import inference_bert
from tokenization_kobert import KoBertTokenizer

def bert_predict(sentence):

    tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')
    model = settings.MODEL_KOBERT

    result_bert = inference_bert.predict_sentiment(sentence, tokenizer, model)

    return result_bert

def image_predict(image):
    model = settings.MODEL_IMAGE
    img_height = 250
    img_width = 250
    image_resize = image.resize((img_height,img_width))
    img_array = np.array(image_resize)
    img_array = img_array.reshape(1,img_height,img_width,3)
    result_image = model.predict(img_array)

    return result_image


def weighted_sum(text_pred, image_pred):
    # text_pred 중립과 긍정 위치 변경 (부정, 중립, 긍정 순이 알아보기 편할 거 같아 변경했습니다.)
    temp_list = []
    temp_list.append(text_pred[0][0])
    temp_list.append(text_pred[0][2])
    temp_list.append(text_pred[0][1])
    text_result = np.array([temp_list])  # 부정, 중립, 긍정
    image_result = image_pred  # 부정, 중립, 긍정
    print("텍스트 결과[부정,중립,긍정]:",text_result, "이미지 결과[부정,중립,긍정]:",image_result)

    # 가중치
    high_wv = 0.8
    low_wv = 0.2
    mid_wv = 0.5
    # 이미지 분류 결과 긍정 혹은 부정이 0.9 이상인 경우 이미지 예측 결과에 높은 가중치 적용(중립 제외)
    if image_result[0][0] >= 0.9 or image_result[0][2] >= 0.9:
        weighted_image = image_result * high_wv
        weighted_text = text_result * low_wv
        weighted_result = weighted_image + weighted_text
    else:
        weighted_image = image_result * mid_wv
        weighted_text = text_result * mid_wv
        weighted_result = weighted_image + weighted_text
    print("최종 결과[부정,중립,긍정]:", weighted_result)
    return weighted_result


def show_results(weighted_result):
    predicted_class = ['부정', '중립', '긍정'][np.argmax(weighted_result, axis=1)[0]]
    if predicted_class == '부정' :
        if weighted_result[0][0] <= 0.6:
            color = 'F10086'
            emoji = "emoji/bad1.jpg"
        elif 0.6 < weighted_result[0][0] <= 0.8:
            color = '711A75'
            emoji = "emoji/bad2.jpg"
        else:
            color = '180A0A'
            emoji = "emoji/bad3.jpg"

    elif predicted_class == '중립':
        if weighted_result[0][1] <= 0.6:
            color = 'D9D7F1'
            emoji = "emoji/neutral1.jpg"
        elif 0.6 < weighted_result[0][1] <= 0.8:
            color = 'FFFDDE'
            emoji = "emoji/neutral2.jpg"
        else:
            color = 'E7FBBE'
            emoji = "emoji/neutral3.jpg"

    else:
        if weighted_result[0][2] <= 0.6:
            color = 'FAD4D4'
            emoji = "emoji/good1.jpg"
        elif 0.6 < weighted_result[0][2] <= 0.8:
            color = 'EF9F9F'
            emoji = "emoji/good2.jpg"
        else:
            color = 'F47C7C'
            emoji = "emoji/good3.jpg"

    return color, emoji

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
            temp_diary.save()

            # prediction
            img = Image.open(settings.MEDIA_ROOT_URL + settings.MEDIA_URL + str(temp_diary.image)).convert('RGB')
            bert_pred = bert_predict(temp_diary.content)
            image_pred = image_predict(img)
            pred = weighted_sum(bert_pred, image_pred)
            color, emoji = show_results(pred)
            temp_diary.negative = np.round(pred[0][0], 2)
            temp_diary.neutral = np.round(pred[0][1], 2)
            temp_diary.positive = np.round(pred[0][2], 2)
            temp_diary.color = color
            temp_diary.emoji= emoji

            temp_diary.save()

            return super().form_valid(form)
        except IntegrityError:
            messages.warning(self.request, "이미 같은 날짜에 일기가 생성되어 있습니다. ")
            return redirect('diaries:list')

    def form_invalid(self, form):
        messages.error(self.request, "양식을 잘못 입력하셨습니다")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('diaries:list')

@method_decorator(login_required(login_url="/accounts/login/"), 'get')
class DiaryListView(ListView):
    model = Diary
    context_object_name = 'diary_list'
    template_name = 'diaryapp/list.html'
    paginate_by = 12

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
        temp_diary = form.save(commit=False)
        temp_diary.writer = self.request.user
        temp_diary.save()

        # prediction
        img = Image.open(settings.MEDIA_ROOT_URL + settings.MEDIA_URL + str(temp_diary.image)).convert('RGB')
        bert_pred = bert_predict(temp_diary.content)
        image_pred = image_predict(img)
        pred = weighted_sum(bert_pred, image_pred)
        color, emoji = show_results(pred)
        temp_diary.negative = np.round(pred[0][0], 2)
        temp_diary.neutral = np.round(pred[0][1], 2)
        temp_diary.positive = np.round(pred[0][2], 2)
        temp_diary.color = color
        temp_diary.emoji = emoji

        temp_diary.save()

        return super().form_valid(form)

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

@method_decorator(login_required(login_url="/accounts/login/"), 'get')
@method_decorator(login_required(login_url="/accounts/login/"), 'post')
@method_decorator(diary_ownership_required, 'get')
@method_decorator(diary_ownership_required, 'post')
class DiaryDeleteView(DeleteView):
    model = Diary
    context_object_name = 'diary_list'
    success_url = reverse_lazy('diaries:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)