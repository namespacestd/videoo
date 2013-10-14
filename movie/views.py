# Create your views here.
from django.shortcuts import render
from ase1.models import Movie
from django.http import HttpResponseServerError
from django.views.defaults import server_error

import logging

logger = logging.getLogger('root.' + __name__)

def detail(request, id):
    try:
        movie = Movie.get_details(id)
        return render(request, 'movie/detail.html', {
            'movie': movie,
        })
    except:
        logger.exception('Failed to retrieve movie details')
        return server_error(request, 'errors/movie_not_found.html')
        #return HttpResponseServerError('Unable to get movie detail.')
