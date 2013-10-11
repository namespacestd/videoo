# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'main/index.html', {
        'form': UserCreationForm(),
        'message': 'Get'
    })