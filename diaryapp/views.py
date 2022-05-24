from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView
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
        return reverse('homes:home')


class DiaryListView(ListView):
    model = Diary
    context_object_name = 'diary_list'
    template_name = 'diaryapp/list.html'
    paginate_by = 21

class DiaryDetailView(DetailView):
    model = Diary
    context_object_name = 'target_diary'
    template_name = 'diaryapp/detail.html'
