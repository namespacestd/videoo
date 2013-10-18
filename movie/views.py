# Create your views here.
from django.shortcuts import render
from ase1.models import Movie, Review, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.views.defaults import server_error

import logging

logger = logging.getLogger('root.' + __name__)

def detail(request, id):
    try:
        movie = Movie.get_details(id)
        return render(request, 'movie/detail.html', {
            'movie': movie,
            'movie_id' : id,
            'all_reviews': Review.objects.filter(movie=Movie.objects.filter(m_id=id)[0]),
            'form': AuthenticationForm(),
            'message': 'Get',
            'logged_in_message': 'Current Username: %s' % request.user.username,
            'username' : request.user.username, 
            'users': User.objects.all(),
            'is_authenticated': request.user.is_authenticated()
        })
    except:
        logger.exception('Failed to retrieve movie details')
        return server_error(request, 'errors/movie_not_found.html')
        #return HttpResponseServerError('Unable to get movie detail.')

def search(request):
    search_term = request.GET['q']
    return render(request, 'movie/search.html', {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated(),
        'movie_results': Movie.search(search_term),
        'user_results': Profile.find(search_term),
        'search_term': search_term
    })