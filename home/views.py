# Create your views here.
from django.shortcuts import render
from ase1.models import Movie


def index(request):
    return render(request, 'main/index.html', {
        'popular_movie_list': Movie.get_popular()['items'][:6],
    })