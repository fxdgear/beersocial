from django.template import Library, Variable, Node, TemplateSyntaxError, loader, Context
from django.db.models import get_model
import datetime
import re

from django.utils.safestring import mark_safe
from django import template

from socialbeer.core.models import Challenge
     
register = Library()

class RandomContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = int(num), varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        limit = int(self.num) + 10
        photos = []
        oembeds = self.model._default_manager.all().order_by('?')[:limit]
        for embed in oembeds:
            photo = {}
            try:
                photo['title'] = eval(embed.response_json)['title']
                photo['thumbnail_url'] = eval(embed.response_json)['thumbnail_url']
                photo['url'] = eval(embed.response_json)['url']
                photo['width'] = eval(embed.response_json)['thumbnail_width']
                photos.append(photo)
            except:
                pass
        context[self.varname] = photos[:self.num] 
        return ''
 
def get_random(parser, token):
    """
    {% get_random appname.Model num as varname %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_random tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return RandomContentNode(bits[1], bits[2], bits[4])

     
class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
 
def get_latest(parser, token):
    """
    {% get_latest appname.Model 20 as varname %}
    """

    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

class RenderContentNode(Node):
    def __init__(self, post, template):
        try:
            self.post = Variable(post)
            self.template = "%s_post_detail.html" % template
        except DoesNotExist:
            raise 

    
    def render(self, context):
        post = self.post.resolve(context)
        t = loader.get_template(self.template)
        c = Context({"post": post})

        return t.render(c)
 
def render_content(parser, token):
    """
    {% render_content for obj as <type> %}
    """

    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "render_content tag takes exactly four arguments"
    if bits[1] != 'for':
        raise TemplateSyntaxError, "first argument to render_content tag must be 'for'"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to render_content tag must be 'as'"

    return RenderContentNode(bits[2], bits[4])


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
    text = pattern.sub(link,text)
    
    return mark_safe(text)


render_content = register.tag(render_content)
get_current_theme = register.tag(get_current_theme)    
get_latest = register.tag(get_latest)
get_random = register.tag(get_random)
