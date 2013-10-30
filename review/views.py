# Create your views here.
from django.http import *
from ase1.models import Review, Movie, Profile
from datetime import datetime


def submit_review(request):
    if request.method == 'POST':
        current_date = datetime.today()
        body = request.POST['review_body']
        title = request.POST['review_title']
        current_user = Profile.objects.filter(user=request.user)[0]
        current_movie = Movie.objects.filter(m_id=int(request.POST['movie_id']))[0]

        already_exists = Review.objects.filter(movie=current_movie, user=current_user)
        
        if not len(already_exists):
            new_review = Review(review_title=title,
                                date_created=current_date,
                                date_edited=None,
                                review_body=body,
                                user=current_user,
                                movie=current_movie)
            new_review.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def edit_review(request, review_id):
    if request.method == 'POST':
        new_title = request.POST['new_review_title']
        new_body = request.POST['new_review_body']
        current_user = Profile.get(request.user)
        current_movie = Movie.objects.filter(m_id=review_id)[0]
        review = Review.objects.filter(user=current_user, movie=current_movie)[0]

        review.approved = False
        review.review_title = new_title
        review.review_body = new_body
        review.date_edited = datetime.today()
        review.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])   
    else:
        return HttpResponse("Unknown edit review request")


def delete_review(request, review_id):
    current_user = Profile.objects.filter(user=request.user)[0]
    current_movie = Movie.objects.filter(m_id=review_id)[0]
    review = Review.objects.filter(user=current_user, movie=current_movie)[0]
    review.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def admin_delete_review(request, target_user, review_id):
    current_user = Profile.find(target_user)[0]
    current_movie = Movie.objects.filter(m_id=review_id)[0]
    review = Review.objects.filter(user=current_user, movie=current_movie)[0]
    review.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def admin_approve_review(request, target_user, review_id):
    current_user = Profile.find(target_user)[0]
    current_movie = Movie.objects.filter(m_id=review_id)[0]
    review = Review.objects.filter(user=current_user, movie=current_movie)[0]
    review.approved = True
    review.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
