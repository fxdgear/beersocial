from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.conf import settings

from beersocial.posts.models import Post

POSTS_PER_PAGE = getattr(settings, "POSTS_PER_PAGE", 25)

def homepage(request, *args, **kwargs):
    template = kwargs.pop('template', "homepage.html")
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 25)

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

