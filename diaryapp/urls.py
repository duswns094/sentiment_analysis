from django.urls import path
from diaryapp.views import DiaryCreateView, DiaryListView, DiaryDetailView

app_name = 'diaries'

urlpatterns = [
    path('create/', DiaryCreateView.as_view(), name="create"),
    path('list/', DiaryListView.as_view(), name="list"),
    path('detail/',DiaryDetailView.as_view(), name="detail"),
]