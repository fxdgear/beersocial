from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from socialregistration.urls import urlpatterns as socialreg_urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socialbeers.views.home', name='home'),
    # url(r'^socialbeers/', include('socialbeers.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'socialbeer.posts.views.homepage'),
    (r'^accounts/', include('members.urls')),
    
)

urlpatterns = urlpatterns + socialreg_urls + staticfiles_urlpatterns()

if settings.DEBUG:
        urlpatterns += patterns('',
            (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
        )