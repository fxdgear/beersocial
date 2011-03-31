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

    status = models.BooleanField(default=True)

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