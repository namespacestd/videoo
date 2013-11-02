from django.conf.urls import patterns, url
from profile import views

urlpatterns = patterns('',
    url(r'^set_user_priority/$', views.set_user_priority, name='set_user_priority'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^lists/(?P<username>\w+)/+$', views.lists, name='lists'),
    url(r'^main$', views.main, name='main'),
    url(r'^lists/quick_add$', views.lists_quick_add, name='lists_quick_add'),
    url(r'^(?P<username>\w+)/+$', views.user_main, name='user_main'),
    url(r'^friends_list/(?P<username>\w+)/+$', views.friends_list, name='friends_list'),
    url(r'^admin_page$', views.admin_page, name='admin_page'),

)
