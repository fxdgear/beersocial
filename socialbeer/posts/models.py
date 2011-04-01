from urllib import urlencode
from httplib2 import Http
import re
from lxml import etree

from django.db import models
from django.contrib.auth.models import User

from socialbeer.beers.models import Beer

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True)
    tweeter_name = models.CharField(max_length=100, blank=True, null=True)
    tweeter_id = models.BigIntegerField(blank=True, null=True)
    tweeter_profile_image = models.URLField(blank=True, null=True)
    tweet_id = models.BigIntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    

    beer = models.ForeignKey(Beer, blank=True, null=True)

    live = models.BooleanField(default=True, help_text="Checked box means the post is live on the site")

    class Meta:
        ordering = ["-pub_date"]

    def __unicode__(self):
        if self.author:
            return "Post: '%s' by %s on %s" % (self.content[:20], self.author.username, self.pub_date)
        else:
            return "Post: '%s' by %s on %s" % (self.content[:20], self.tweeter_name, self.pub_date)

    @property
    def tweet_url(self):
        return "http://twitter.com/%s/status/%d" %( self.tweeter_name, self.tweet_id)
    
    @property
    def post_author(self):
        if self.author:
            return self.author
        else:
            return self.tweeter_name
    
    @property
    def author_url(self):
        if self.author:
            return self.author.get_absolute_url()
        else:
            return "http://twitter.com/%s/" % self.tweeter_name

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        urls = re.findall(r'(https?://\S+)', self.content)
        if urls:
            for url in urls:
                h = Http()
                api_url = "http://api.longurl.org/v2/expand"
                params = urlencode({"url":url})
                r,c = h.request(("%s?%s"%(api_url,params)), "GET")
                print r,c
                if r.status == 200:
                    x = etree.XML(c)
                    results = x.xpath("/response/long-url/text()")
                    if results:
                        self.content = self.content.replace(url, results[0])
        
        super(Post, self).save()






