__author__ = 'matt'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^create$', views.create, name='create'),
)