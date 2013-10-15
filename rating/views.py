
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

def add_to_list(request):
    if request.method == 'POST':
        movie_status = request.POST['movie_status']
        movie_title = request.POST['movie_title']
        movie_rating = request.POST['movie_rating']

        print movie_status
        print movie_title
        print movie_rating

    return HttpResponseRedirect(request.META['HTTP_REFERER'])