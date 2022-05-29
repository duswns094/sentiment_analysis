from django.urls import path
from diaryapp.views import DiaryCreateView, DiaryListView, DiaryDetailView, DiaryUpdateView, DiaryCalendarView, \
    DiaryDeleteView

app_name = 'diaries'

urlpatterns = [
    path('create/', DiaryCreateView.as_view(), name="create"),
    path('list/', DiaryListView.as_view(), name="list"),
    path('calendar',DiaryCalendarView.as_view(), name='calendar'),
    path('detail/<int:pk>', DiaryDetailView.as_view(), name="detail"),
    path('update/<int:pk>', DiaryUpdateView.as_view(), name="update"),
    path('delete/<int:pk>', DiaryDeleteView.as_view(), name="delete"),
]