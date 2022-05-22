from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from . import views # 같은 폴더 내의 views.py를 import

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")

]