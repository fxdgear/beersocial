from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('socialbeer.posts.views',
    (r'^$', 'post_list'),
    (r'^(?P<post_id>[-\w]+)/$', 'post_detail', {}, 'posts_post_detail'),   
)