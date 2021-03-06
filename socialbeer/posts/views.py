from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page

from socialbeer.posts.models import Post

POSTS_PER_PAGE = getattr(settings, "POSTS_PER_PAGE", 25)

@cache_page(60*5)
def homepage(request, *args, **kwargs):
    template = kwargs.pop('template', "homepage.html")
    post_list = Post.objects.published()
    paginator = Paginator(post_list, POSTS_PER_PAGE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)

    return render_to_response(template, {
        'posts': posts,
    }, RequestContext(request))


def post_detail(request, post_id, *args, **kwargs):
    template = kwargs.pop('template', 'posts/post_detail.html')
    post = Post.objects.get(pk=post_id)

    return render_to_response(template, {
        'post': post,
    }, RequestContext(request))

def post_list(request, id, *args, **kwargs):
    pass