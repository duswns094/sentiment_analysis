from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Carausel


# Create your views here.

@login_required(login_url="/accounts/login/")
def index(request):
    obj = Carausel.objects.all()
    context = {
        'obj':obj
    }
    return render(request, 'homeapp/index.html', context)
# Create your views here