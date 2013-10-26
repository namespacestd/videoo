from django.http import *
from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.forms import *
from ase1.models import *
from movie.views import get_review_approvals

def main(request):
    return render(request, 'profile/main.html', {
            'username': request.user.username,
            'is_authenticated': request.user.is_authenticated(),
            'all_reviews': get_review_approvals(request, Review.objects.filter(user=Profile.get(request.user))), 
        })

def login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AuthenticationForm(request.POST) # A form bound to the POST data
        print request.META['HTTP_REFERER']

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                #if request.POST.get('next', False):
                 #   return HttpResponseRedirect(request.POST.get('next'))
                #else:
                return HttpResponseRedirect(request.META['HTTP_REFERER']) # (settings.LOGIN_REDIRECT_URL)
            else:
                message = 'Your account has been disabled.'
        else:
            message = "Your username and password didn't match. Please try again."

        # TODO: Handle error better than just returning a blank page
        return HttpResponse(message)
    else:
        return HttpResponse("No login page. Must be posted to by login form.")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
    # return HttpResponse("Logout handler")


def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CreateAccountForm(request.POST)
        try:
            if form.is_valid():
                profile = form.save()
                user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
                auth.login(request, user)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])# TODO: Redirect to user profile page
            else:
                raise Exception(form.errors)
        except Exception as ex:
            return render(request, 'profile/create.html', {
                'form': form,
                'message': ex
            })
    else:
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