# Create your views here.
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from ase1.models import Movie, CreateAccountForm


def index(request):
    return render(request, 'main/index.html', {
        'popular_movie_list': Movie.get_popular()['items'][:6]
    })