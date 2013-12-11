from django.conf.urls import patterns, url
from review import views

urlpatterns = patterns('',

    url(r'^submit_review$', views.submit_review),
    url(r'^edit_review/(?P<review_id>\d+)/?$', views.edit_review),
    url(r'^delete_review/(?P<id>\d+)/?$', views.delete_review),
    url(r'^approve_review/(?P<id>\d+)/?$', views.approve_review),

)