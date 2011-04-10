from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

from socialbeer.members.signals import create_profile
from socialbeer.posts.models import Post

from socialregistration.models import OpenIDProfile, TwitterProfile, FacebookProfile

class Profile(models.Model):
    # each profile is associated to a User
    user = models.ForeignKey(User)

    # Will hold more information here about users


    @property
    def full_name(self):
        if self.user.firstname and self.user.lastname:
            return "%s %s" % (self.user.firstname, self.user.lastname)
        elif self.user.firstname or self.user.lastname:
            return "%s%s" % (self.user.firstname, self.user.lastname)
        else:
            return "%s" % self.user

    def __unicode__(self):
        return "%s" % self.user
    
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





 
# When model instance is saved, trigger creation of corresponding profile
signals.post_save.connect(create_profile, sender=User)
