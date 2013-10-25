# Create your views here.
from django.http import *
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from ase1.models import Review, Movie, Profile
from datetime import date

def submit_review(request):
    if request.method == 'POST':
        current_date = date.today()
        body = request.POST['review_body']
        current_user = Profile.objects.filter(user=request.user)[0]
        current_movie = Movie.objects.filter(m_id=int(request.POST['movie_id']))[0]

        already_exists = Review.objects.filter(movie=current_movie, user=current_user)
        
        if list(already_exists) == []:
            new_review = Review(date_created=current_date, review_body=body, user=current_user, movie=current_movie)
            new_review.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("No login page. Must be posted to by login form.")

def edit_review(request, id):
    if request.method == 'POST':
        new_body = request.POST['new_review_body']
        current_user = Profile.objects.filter(user=request.user)[0]
        current_movie = Movie.objects.filter(m_id=id)[0]
        review = Review.objects.filter(user=current_user, movie=current_movie)[0]

        review.review_body = new_body
        review.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])   
    else:
        return HttpResponse("Unknown edit review request")