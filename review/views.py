# Create your views here.
from django.http import *
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from ase1.models import Review, Movie, Profile, CreateAccountForm
from datetime import date

def submit_review(request):
    if request.method == 'POST':
        current_date = date.today()
        body = request.POST['review_body']
        title = request.POST['review_title']
        current_user = Profile.objects.filter(user=request.user)[0]
        current_movie = Movie.objects.filter(m_id=int(request.POST['movie_id']))[0]

        already_exists = Review.objects.filter(movie=current_movie, user=current_user)
        
        if list(already_exists) == []:
            new_review = Review(review_title=title, date_created=current_date, review_body=body, user=current_user, movie=current_movie)
            new_review.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def edit_review(request, id):
    if request.method == 'POST':
        new_title = request.POST['new_review_title']
        new_body = request.POST['new_review_body']
        current_user = Profile.objects.filter(user=request.user)[0]
        current_movie = Movie.objects.filter(m_id=id)[0]
        review = Review.objects.filter(user=current_user, movie=current_movie)[0]

        review.review_title = new_title
        review.review_body = new_body
        review.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])   
    else:
        return HttpResponse("Unknown edit review request")

def delete_review(request, id):
    current_user = Profile.objects.filter(user=request.user)[0]
    current_movie = Movie.objects.filter(m_id=id)[0]
    review = Review.objects.filter(user=current_user, movie=current_movie)[0]
    review.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])