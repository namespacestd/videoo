# Create your views here.
from django.shortcuts import render
from movie.models import Movie

def detail(request, id):
    return render(request, 'movie/detail.html', {
        'movie': Movie.get_details(id),
    })