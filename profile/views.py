from django.http import *
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.forms import *
from ase1.models import *
from movie.views import get_review_approvals
from django.db.models import Q
from datetime import timedelta, date
import logging

logger = logging.getLogger('root.' + __name__)


def user_main(request, username):
    target_user = Profile.find(username)

    if not len(target_user):
        return HttpResponse(status=404)

    target_user = target_user[0]

    class Stats: pass

    stats = Stats()
    stats.join_date = target_user.join_date
    all_reviews = Review.objects.filter(user=target_user)
    stats.num_reviewed = len(all_reviews)
    watched = MovieList.objects.filter(user=target_user, status='Completed')
    stats.num_watched = len(watched)
    all_ratings = Rating.objects.filter(user=target_user)
    stats.num_rated = len(all_ratings)

    sorted_objs = sorted(list(all_reviews), key=lambda x: x.date_created)
    # Only reviews posted in the last month are displayed
    stats.recent_reviews = filter(lambda x: date.today() - x.date_created < timedelta(30), sorted_objs)

    return render(request, 'profile/main.html', {
        'current_user': username,
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated(),
        'is_administrator' : request.user.is_superuser,   
        'all_reviews': get_review_approvals(request, Review.objects.filter(user=target_user)),
        'user_stats': stats,
    })


def main(request):
    return render(request, 'profile/main.html', {
        'all_reviews': get_review_approvals(request, Review.objects.filter(user=Profile.get(request.user))),
        'is_administrator' : request.user.is_superuser,
    })


def login(request):
    if request.method == 'POST':  # If the form has been submitted...
        AuthenticationForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse('Success')
            else:
                error_msg = 'Your account has been disabled.'
        else:
            error_msg = 'Your username and password didn\'t match. Please try again.'

        logger.info('Login failed. User: %s, Reason: %s', username, error_msg)
        return HttpResponse(error_msg)
    else:
        return HttpResponse('No login page. Must be posted to by login form.')


def logout(request):
    user = request.user
    auth.logout(request)
    logger.info('Logout. User: %s', user)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = CreateAccountForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password2'])
                auth.login(request, user)

                logger.info('User Create successful. User: %s', form.cleaned_data['username'])
                return HttpResponse('Success')  # Redirects to user's profile page
            else:
                logger.error('User Create failed. Invalid form.')
                raise Exception(form.errors.as_ul())
        except Exception as ex:
            logger.error('User Create failed. Validation or Authentication failed.')
            return HttpResponse(ex.message)
    else:
        logger.error('User Create failed. Invalid form submission.')
        return HttpResponse('Account creation failed.')


def userlist(request, username):
    target_user = Profile.find(username)[0]
    currently_planned = MovieList.objects.filter(user=target_user, status='Plan to Watch')
    completed = MovieList.objects.filter(user=target_user, status='Watched')

    return render(request, 'profile/userlist.html', {
        'planned': currently_planned,
        'completed': completed,
        'is_administrator' : request.user.is_superuser,
    })


def friends_list(request, username):
    return HttpResponseRedirect(request.META['HTTP_REFERER']) 


def admin_page(request):
    return render(request, 'profile/admin_page.html', {
        'is_administrator' : request.user.is_superuser,
        'all_users' : Profile.objects.all(),
        'unapproved_reviews' : get_review_approvals(request, Review.objects.filter(Q(approved=None) | Q(approved=False)))
    })


def set_user_priority(request):
    if request.method == 'POST':
        for profile in Profile.objects.all():
            set_to_superuser = request.POST.__contains__(profile.user.username)
            if set_to_superuser:
                profile.set_to_superuser(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER']) 


def userlist_quickadd(request):
    if request.method == 'POST':
        movie_status = request.POST['movie_status']
        current_user = Profile.get(request.user)
        movie = Movie.objects.filter(m_id=request.POST['movie_id'])[0]
        current_rating = Rating.objects.filter(user=current_user, movie=movie)

        if not len(current_rating):
            current_rating = Rating(user=current_user, movie=movie, rating=-1)
            current_rating.save()

        already_exists = MovieList.objects.filter(user=current_user, movie=movie)

        if not len(already_exists):
            new_entry = MovieList(rating=current_rating[0],
                                  movie=movie,
                                  user=Profile.get(request.user),
                                  status=movie_status)
            new_entry.save()
        else:
            existing_entry = already_exists[0]
            existing_entry.status = movie_status
            existing_entry.rating = current_rating[0]
            existing_entry.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])