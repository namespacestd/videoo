
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from ase1.models import Movie, Profile, ReviewRating, Review, CreateAccountForm


def add_to_list(request):
    if request.method == 'POST':
        movie_status = request.POST['movie_status']
        movie_title = request.POST['movie_title']
        movie_rating = request.POST['movie_rating']

        print movie_status
        print movie_title
        print movie_rating

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def rate(request, rating_id, approve):
    target_user = Profile.find(request.GET['review_of'])
    target_movie = Movie.objects.filter(m_id=int(rating_id))[0]
    review_of = Review.objects.filter(movie=target_movie, user=target_user)[0]
    user = Profile.get(request.user)

    already_exists = ReviewRating.objects.filter(review=review_of, user=user)

    """for entry in already_exists:
        entry.delete()"""
    
    if not len(already_exists):
        review_rating = ReviewRating(review=review_of, user=user, vote=approve)
        review_rating.save()
    else:
        if already_exists[0].vote == int(approve):
            already_exists[0].delete()
        else:
            already_exists[0].vote = approve
            already_exists[0].save()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])