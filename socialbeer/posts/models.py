from django.db import models
from django.contrib.auth.models import User

from socialbeer.beers.models import Beer

class PostManager(models.Manager):
    def published(self):
        return self.filter(live=True, retweet=False)


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True)
    tweet_id = models.BigIntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    parent_post = models.ForeignKey('self', blank=True, null=True)
    retweets = models.ManyToManyField('self', blank=True, null=True)
    retweet = models.BooleanField(default=False)
    
    beer = models.ForeignKey(Beer, blank=True, null=True)

    live = models.BooleanField(default=True, help_text="Checked box means the post is live on the site")

    objects = PostManager()

    class Meta:
        ordering = ["-pub_date"]

    def __unicode__(self):
        if self.author:
            return "Post: '%s' by %s on %s" % (self.content[:20], self.author, self.pub_date)
        else:
            return "Post: '%s' by %s on %s" % (self.content[:20], self.tweeter_name, self.pub_date)

    @models.permalink
    def get_absolute_url(self):
        return ('socialbeer.posts.views.post_detail', (), { 'post_id': self.pk } )

    @property
    def retweet_count(self):
        return self.retweets.all().count()

    @property
    def tweet_url(self):
        return "http://twitter.com/%s/status/%d" %( self.author.twitter_name, self.tweet_id)
    
    @property
    def post_author(self):
        return self.author.get_profile()
    
    @property
    def author_url(self):
        if self.author:
            return self.author.get_profile().get_absolute_url()
        else:
            return "http://twitter.com/%s/" % self.author.get_profile()
    
    @property
    def children(self):
        return Post.objects.filter(parent_post=self, live=True)






