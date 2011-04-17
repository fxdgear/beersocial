from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.contrib.auth.signals import user_logged_in

from tweepy.api import API

from socialbeer.members.signals import create_profile
from socialbeer.posts.models import Post

from socialregistration.models import OpenIDProfile, TwitterProfile, FacebookProfile

class Profile(models.Model):
    # each profile is associated to a User
    user = models.ForeignKey(User)
    profile_image = models.ImageField(upload_to="avatars/", blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    twitter_name = models.CharField(max_length=100, blank=True, null=True)


    def get_absolute_url(self):
        return "/accounts/%s" % self.user.__unicode__()

    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def last_name(self):
        return self.user.last_name

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.user.firstname, self.user.lastname)
        elif self.first_name or self.last_name:
            return "%s%s" % (self.first_name, self.last_name)
        else:
            return "%s" % self.user

    def __unicode__(self):
        return "%s" % self.user.__unicode__()
    
    @property
    def twitter_profile(self):
        try:
            return TwitterProfile.objects.get(user=self.user)
        except:
            return None

    @property
    def facebook_profile(self):
        try:
            return FacebookProfile.objects.get(user=self.user)
        except:
            return None

    @property
    def openid_profile(self):
        try:
            return OpenIDProfile.objects.get(user=self.user)
        except:
            return None

    def all_posts(self):
        return Post.objects.published().filter(author=self.user)


def update_twitter_profile( *args, **kwargs):
    a = API()
    user = kwargs.get('user')
    profile = user.get_profile()
    try:
        twitter_user = a.get_user(user_id=profile.twitter_profile.twitter_id)
    except:
        twitter_user = None
    
    if twitter_user:
        profile.user.first_name = twitter_user.name.split(" ")[0]
        profile.user.last_name = twitter_user.name.split(" ")[1:]
        profile.user.save()    

        profile.website = twitter_user.url    
        profile.profile_image_url = twitter_user.profile_image_url    
        profile.description = twitter_user.description    
        profile.twitter_name = twitter_user.screen_name
        profile.save()
 
# When model instance is saved, trigger creation of corresponding profile
signals.post_save.connect(create_profile, sender=User)
user_logged_in.connect(update_twitter_profile)
