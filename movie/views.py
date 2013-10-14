# Create your views here.
from django.shortcuts import render
from ase1.models import Movie, Review
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

def detail(request, id):
    return render(request, 'movie/detail.html', {
        'movie': Movie.get_details(id),
        'movie_id' : id,
        'all_reviews': Review.objects.filter(movie=Movie.objects.filter(m_id=id)[0]),
        'form': AuthenticationForm(),
        'message': 'Get',
        'logged_in_message': 'Current Username: %s' % request.user.username,
        'username' : request.user.username, 
        'users': User.objects.all(),
        'is_authenticated': request.user.is_authenticated()
    })