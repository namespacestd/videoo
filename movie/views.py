# Create your views here.
from django.shortcuts import render
from ase1.models import Movie, Review, Profile, Rating
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.views.defaults import server_error

import logging

logger = logging.getLogger('root.' + __name__)

def detail(request, id):
    try:
        movie = Movie.get_details(id)
        profile = Profile.get(request.user)
        user_rating = 0
        if request.user.is_authenticated():
            user_rating = Rating.get_rating_for_user(profile, movie)
        return render(request, 'movie/detail.html', {
            'movie': movie,
            'movie_id' : id,
            'all_reviews': Review.objects.filter(movie=Movie.objects.filter(m_id=id)[0]),
            'form': AuthenticationForm(),
            'logged_in_message': 'Current Username: %s' % request.user.username,
            'username' : request.user.username,
            'users': User.objects.all(),
            'is_authenticated': request.user.is_authenticated(),
            'user_rating': user_rating
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

def rate(request, id):
    try:
        stars = request.GET['stars']
        movie = Movie.get_details(id)
        user = Profile.get(request.user)
        Rating.set_rating_for_user(movie, stars, user)
        return HttpResponseRedirect('/movie/detail/%s' % id)
    except:
        logger.exception('Failed to submit rating for movie')
        return server_error(request, 'errors/db_error.html')