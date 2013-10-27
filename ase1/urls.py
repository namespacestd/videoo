from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Pattern examples:
# url(r'^$', 'ase1.views.home', name='home')
# url(r'^ase1/', include('ase1.foo.urls'))
urlpatterns = patterns(
    '',
    url(r'^$', 'home.views.index', name='index'),    # Root url for application

    url(r'^movie/', include('movie.urls')),
    url(r'^profile/', include('profile.urls')),
    url(r'^review/', include('review.urls')),
    url(r'^rating/', include('rating.urls')),

    # Static content goes under the '/site_media/' directory
    # url (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()