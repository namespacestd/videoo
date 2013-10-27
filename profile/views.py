from django.http import *
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.forms import *
from ase1.models import *
from movie.views import get_review_approvals
import logging

logger = logging.getLogger('root.' + __name__)


def user_main(request, username):
    target_user = Profile.find(username)

    logger.warning("FOO %d", len(target_user))
    if not len(target_user):
        return HttpResponse(status=404)

    return render(request, 'profile/main.html', {
        'current_user': username,
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated(),
        'all_reviews': get_review_approvals(request, Review.objects.filter(user=target_user[0])),
    })


def main(request):
    return render(request, 'profile/main.html', {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated(),
        'all_reviews': get_review_approvals(request, Review.objects.filter(user=Profile.get(request.user))),
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
    currently_watching = MovieList.objects.filter(user=target_user, status='Watching')
    currently_planned = MovieList.objects.filter(user=target_user, status='Plan to Watch')
    completed = MovieList.objects.filter(user=target_user, status='Completed')

    return render(request, 'profile/userlist.html', {
        'watching': currently_watching,
        'planned': currently_planned,
        'completed': completed,
        'login_form': AuthenticationForm(),
        'signup_form': CreateAccountForm(),
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated()
    })


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