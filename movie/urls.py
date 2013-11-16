from django.conf.urls import patterns, url
from movie import views

urlpatterns = patterns('',

    url(r'^browse/+$', views.browse, name='browse'),
    url(r'^browse-more/+$', views.browse_more, name='browse-more'),  # for infinite scrolling

    # movie detail url: /movie/detail/{id}
    url(r'^detail/(?P<movie_id>\d+)/+$', views.detail, name='detail'),
    url(r'^rate/(?P<movie_id>\d+)/+$', views.rate, name='rate'),

    url(r'^search/+.*$', views.search, name='search'),
    url(r'^search-more/+$', views.search_more, name='search-more'),  # for infinite scrolling

)