from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from diaryapp.decorators import diary_ownership_required
from diaryapp.forms import DiaryCreationForm
from diaryapp.models import Diary



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
            return super().form_valid(form)
        except:
            print("실패")
    #
    def get_success_url(self):
        return reverse('diaries:list')

@method_decorator(login_required(login_url="/accounts/login/"), 'get')
class DiaryListView(ListView):
    model = Diary
    context_object_name = 'diary_list'
    template_name = 'diaryapp/list.html'
    paginate_by = 21
    
    def get_queryset(self):  # 컨텍스트 오버라이딩
        return Diary.objects.filter(writer=self.request.user)

    # def get_context_data(self, **kwargs):
    #     object_list = Diary.objects.filter(writer=self.get_object())
    #     return super(DiaryListView, self).get_context_data(object_list=object_list)

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

    def get_success_url(self):
        return reverse('diaries:detail', kwargs={'pk':self.object.pk})