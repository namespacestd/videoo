from django.http import *
from django.contrib import auth
from django.shortcuts import render
from profile.models import *
from django.contrib.auth.forms import UserCreationForm


def login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CreateAccountForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
                 #TODO: Handle user login: Redirect to user profile page
                return HttpResponse("Successfully logged in. This would usually redirect to the user profile page.")
            else:
                 #TODO: Handle error
                return HttpResponse("Unable to log in.  User does not exist, or is not active.")
    else:
        return HttpResponse("No login page. Must be posted to by login form.")


def logout(request):
    auth.logout()
    return HttpResponse("Logout handler")


def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CreateAccountForm(request.POST)
        try:
            form.clean_username()
            form.clean_password2()
            if form.is_valid():
                user = form.save()
                # TODO: Redirect to user profile page
                return HttpResponse("Account successfully created. This would usually redirect to the user profile page.")
            else:
                return render(request, 'profile/create.html', {
                    'form': form,
                    'message': 'Please fill out all fields, and ensure that passwords match.'
                })
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