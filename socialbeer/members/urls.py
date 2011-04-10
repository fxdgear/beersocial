from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('socialbeer.members.views',
    url(r'^profile/$', 'profile_detail_redirect', name='profiles_profile_detail'),
    (r'^', include('profiles.urls')),   
)