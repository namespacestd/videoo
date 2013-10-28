# Create your views here.
from django.shortcuts import render
from ase1.models import Movie, Review, Profile, Rating, ReviewRating
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.defaults import server_error
from ase1.models import CreateAccountForm

import logging

logger = logging.getLogger('root.' + __name__)


def browse(request):
    # Used to store attributes for use in the html template
    class Dummy(): pass

    logger.info('Loading Browse Page')
    browse_filters = []  # This will hold other categories by which the user can sort

    # Each entry to browse_filters must contain a 'name' field and an 'option_list'
    # Each list item must contain an 'id_' and a 'name'
    genre = Dummy()
    genre.name = 'genre'
    genre.option_list = []
    for obj in Movie.get_genres():
        add = Dummy()
        add.id_ = obj[0]
        add.name = obj[1]
        genre.option_list.append(add)
    if not genre.option_list:
        logger.warning('No Genres Retrieved')
        initial_results = []
    else:
        if request.GET.has_key('genre'):
            selected_genre = [a for a in genre.option_list if a.id_ == int(request.GET['genre'])][0].id_
        else:
            # Gets the first genre so there is something to display
            selected_genre = genre.option_list[0].id_
        results = Movie.get_movies_for_genre(selected_genre)['items']

    browse_filters.append(genre)
    return render(request, 'movie/browse.html', {
        'browse_filters': browse_filters,
        'results_list': results
    })


def detail(request, movie_id):
    try:
        movie = Movie.get_details(movie_id)
        logger.info('Loading Movie Detail Page. Movie: %s', movie.title)
        profile = Profile.get(request.user)
        user_rating = 0
        if request.user.is_authenticated():
            user_rating = Rating.get_rating_for_user(profile, movie)
        return render(request, 'movie/detail.html', {
            'movie': movie,
            'movie_id': movie_id,
            'all_reviews': get_review_approvals(request, Review.objects.filter(movie=movie)),
            'already_reviewed': already_reviewed(movie, profile),
            'user_rating': user_rating
        })
    except:
        logger.exception('Failed to retrieve movie details')
        return server_error(request, 'errors/movie_not_found.html')
        #return HttpResponseServerError('Unable to get movie detail.')


def already_reviewed(current_movie, current_user):
    already_exists = Review.objects.filter(movie=current_movie, user=current_user)
    if not len(already_exists) == []:
        return False
    return True


def get_review_approvals(request, reviews):
    review_approval = []
    for review in reviews:
        is_current_user = (review.user == Profile.get(request.user))
        review_approvals = ReviewRating.objects.filter(review=review)

        count = 0
        for review_rating in review_approvals:
            if review_rating.vote == 0:
                count += 1
        review_approval.append({
            "review": review,
            "is_current_user": is_current_user,
            "upvote": count,
            "downvote": len(review_approvals)-count
        })
    
    return review_approval


def search(request):
    search_term = request.GET['q']
    logger.info('Loading Search Page. Term: %s', search_term)
    return render(request, 'movie/search.html', {
        'movie_results': Movie.search(search_term),
        'user_results': Profile.find(search_term),
        'search_term': search_term,
    })


def rate(request, movie_id):
    try:
        stars = request.GET['stars']
        movie = Movie.get_details(movie_id)
        user = Profile.get(request.user)
        logger.debug('Rating. User: %s. Movie: %s. Stars: %s', user.user.username, movie.m_id, stars)
        Rating.set_rating_for_user(movie, stars, user)
        return HttpResponseRedirect('/movie/detail/%s' % movie_id)
    except:
        logger.exception('Failed to submit rating for movie')
        return server_error(request, 'errors/db_error.html')