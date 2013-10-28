from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^userlist/(?P<username>\w+)/+$', views.userlist, name='userlist'),
    url(r'^main$', views.main, name='main'),
    url(r'^userlist/quick_add$', views.userlist_quickadd, name='userlist_quickadd'),
    url(r'^(?P<username>\w+)/+$', views.user_main, name='user_main'),
    url(r'^friends_list/(?P<username>\w+)/+$', views.friends_list, name='friends_list')
)