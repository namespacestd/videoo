from django.http import *
from django.contrib import auth
from django.shortcuts import render
from profile.models import *
from django.contrib.auth.forms import *


def login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AuthenticationForm(request.POST) # A form bound to the POST data

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                if request.POST.get('next', False):
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return HttpResponseRedirect('/') # (settings.LOGIN_REDIRECT_URL)
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
    return HttpResponse("Logout handler")


def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
                auth.login(request, user)
                return HttpResponse("Account successfully created. This should redirect to the user profile page.")
                # TODO: Redirect to user profile page
            else:
                raise Exception("Invalid username or password")
        except Exception as ex:
            return render(request, 'profile/create.html', {
                'form': form,
                'message': ex
            })
    else:
        return render(request, 'profile/create.html', {
            'form': UserCreationForm(),
            'message': ''
        })