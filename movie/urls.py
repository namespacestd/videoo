from django.conf.urls import patterns, url
from movie import views

urlpatterns = patterns('',

    # movie detail url: /movie/detail/{id}
    url(r'^detail/(?P<id>\d+)/+$', views.detail, name='detail'),
    url(r'^rate/(?P<id>\d+)/+$', views.rate, name='rate'),
    url(r'^search/+.*$', views.search, name='search'),

    #url(r'^logout$', views.logout, name='logout'),
    #url(r'^create$', views.create, name='create'),
)