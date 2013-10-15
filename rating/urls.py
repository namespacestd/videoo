from django.conf.urls import patterns, url
from rating import views

urlpatterns = patterns('',
    url(r'^add_to_list$', views.add_to_list, name='add_to_list'),
)