from django.template import Library, Variable, Node, TemplateSyntaxError, loader, Context
from django.db.models import get_model
import datetime
import re

from django.utils.safestring import mark_safe
from django import template

from socialbeer.core.models import Challenge
     
register = Library()
     
class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

class RenderContentNode(Node):
    def __init__(self, post):
        try:
            self.post = Variable(post)
        except DoesNotExist:
            raise 

    
    def render(self, context):
        post = self.post.resolve(context)
        t = loader.get_template("post_detail.html")
        c = Context({"post": post})

        return t.render(c)
 
def render_content(parser, token):
    """
    {% render_content for obj %}
    """

    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "render_content tag takes exactly two arguments"
    if bits[1] != 'for':
        raise TemplateSyntaxError, "first argument to render_content tag must be 'for'"
    return RenderContentNode(bits[2])


class CurrentThemeNode(Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        today = datetime.datetime.today()
        challenges = Challenge.objects.filter(start_date__lte=today, end_date__gte=today)
        if len(challenges):
            context[self.varname] = challenges[0]
        return ''

def get_current_theme(parser, token):
    """
    {% get_current_theme as theme %}
    """

    bits = token.contents.split()
    if len(bits) !=3:
        raise TemplateSyntaxError, "you fucked up"
    
    return CurrentThemeNode(bits[2])


register = template.Library()

@register.filter(name='twitterfy')
def twitterfy(tweet):
    
    # find hashtags
    pattern = re.compile(r"(?P<start>.?)#(?P<hashtag>[A-Za-z_]+)(?P<end>.?)")
    
    # replace with link to search
    link = r'\g<start>#<a href="http://search.twitter.com/search?q=\g<hashtag>"  title="#\g<hashtag> search Twitter">\g<hashtag></a>\g<end>'
    text = pattern.sub(link,tweet)
    
    # find usernames
    pattern = re.compile(r"(?P<start>.?)@(?P<user>[A-Za-z0-9_]+)(?P<end>.?)")
    
    # replace with link to profile
    link = r'\g<start>@<a href="http://twitter.com/\g<user>"  title="@\g<user> on Twitter">\g<user></a>\g<end>'
    text = pattern.sub(link,tweet)
    
    return mark_safe(text)


render_content = register.tag(render_content)
get_current_theme = register.tag(get_current_theme)    
get_latest = register.tag(get_latest)
