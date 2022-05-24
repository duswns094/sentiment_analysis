from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


# Create your views here.

@login_required(login_url="/accounts/login/")
def index(request):

    return render(request, 'homeapp/index.html', {})


