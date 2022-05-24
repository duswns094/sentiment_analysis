from django.urls import path
from diaryapp.views import DiaryCreateView, DiaryListView, DiaryDetailView, DiaryUpdateView

app_name = 'diaries'

urlpatterns = [
    path('create/', DiaryCreateView.as_view(), name="create"),
    path('list/', DiaryListView.as_view(), name="list"),
    path('detail/<int:pk>', DiaryDetailView.as_view(), name="detail"),
    path('update/<int:pk>', DiaryUpdateView.as_view(), name="update"),

]