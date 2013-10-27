# Create your views here.
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from ase1.models import Movie, CreateAccountForm


def index(request):
    return render(request, 'main/index.html', {
        'login_form': AuthenticationForm(),
        'signup_form': CreateAccountForm(),
        'username': request.user.username,
        'message': 'Get',
        'logged_in_message': 'Current Username: %s' % request.user.username,
        'users': User.objects.all(),
        'is_authenticated': request.user.is_authenticated(),
        'popular_movie_list': Movie.get_popular()['items'][:6]
    })