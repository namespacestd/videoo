# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from ase1.models import CreateAccountForm


def index(request):
    return render(request, 'main/index.html', {
        'login_form': AuthenticationForm(),
        'signup_form': CreateAccountForm(),
        'username': request.user.username,
        'message': 'Get',
        'logged_in_message': 'Current Username: %s' % request.user.username,
        'users': User.objects.all(),
        'is_authenticated': request.user.is_authenticated()
    })