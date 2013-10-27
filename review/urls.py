from django.conf.urls import patterns, url
from review import views

urlpatterns = patterns('',

    # movie detail url: /movie/detail/{id}
    url(r'^submit_review$', views.submit_review),
    url(r'^edit_review/(?P<review_id>\d+)/$', views.edit_review),
    url(r'^delete_review/(?P<review_id>\d+)/$', views.delete_review),

    #url(r'^logout$', views.logout, name='logout'),
    #url(r'^create$', views.create, name='create'),
)