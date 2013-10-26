from django.http import *
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.forms import *
from ase1.models import *
from movie.views import get_review_approvals
import logging

logger = logging.getLogger('root.' + __name__)


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
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                error_msg = 'Your account has been disabled.'
        else:
            error_msg = 'Your username and password didn\'t match. Please try again.'

        # TODO: Handle error better than just returning a blank page
        logger.info('Login failed. User: %s, Reason: %s', username, error_msg)
        return HttpResponse(error_msg)
    else:
        return HttpResponse('No login page. Must be posted to by login form.')


def logout(request):
    user = request.user
    auth.logout(request)
    logger.info('Logout. User: %s', user)
    return HttpResponseRedirect('/')


def create(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = CreateAccountForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password2'])
                auth.login(request, user)

                logger.info('User Create successful. User: %s', form.cleaned_data['username'])
                return redirect('/profile/main')  # Redirects to user's profile page
            else:
                logger.error('User Create failed. Invalid form.')
                raise Exception(form.errors)
        except Exception as ex:
            logger.error('User Create failed. Validation or Authentication failed.')
            return render(request, 'profile/create.html', {
                'form': form,
                'message': ex
            })
    else:
        logger.error('User Create failed. Invalid form submission.')
        return render(request, 'profile/create.html', {
            'form': CreateAccountForm(),
            'message': ''
        })


def userlist(request):
    return render(request, 'profile/userlist.html', {
        'login_form': AuthenticationForm(),
        'signup_form': CreateAccountForm(),
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated()
    })


def userlist_quickadd(request):
    return HttpResponseRedirect(request.META['HTTP_REFERER'])