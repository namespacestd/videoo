# Create your views here.
from django.http import HttpResponse

def login(request):
    return HttpResponse("Login handler")

def logout(request):
    return HttpResponse("Logout handler")

def create(request):
    return HttpResponse("Create account page")
