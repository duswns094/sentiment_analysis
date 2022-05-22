from django.urls import path
from homeapp import views


app_name = 'homes'

urlpatterns = [
    path('', views.index, name='home'),
]