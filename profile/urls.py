from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^create$', views.create, name='create'),
)