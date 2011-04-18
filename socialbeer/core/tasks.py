from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from celery.decorators import task

from socialbeer.posts.models import Post
from socialbeer.core.utils import expand_urls
from socialbeer.members.models import Profile
from socialregistration.models import TwitterProfile

        
@task()
def process_tweet(status, *args, **kwargs):

    try:
        profile = Profile.objects.get(user__twitterprofile__twitter_id=status.user.id)
    except:
        user,created = User.objects.get_or_create(username=status.author.screen_name)
        twitter_profile, created = TwitterProfile.objects.get_or_create(user=user, site=Site.objects.get_current(), twitter_id=status.user.id)
        profile = Profile.objects.get(user=user, user__twitterprofile=twitter_profile)

    try:
        obj, created = Post.objects.get_or_create(author=profile.user, tweet_id=status.id)
    except:
        created=False

    if created:
        if status.in_reply_to_status_id:
            try:
                obj.parent_post = Post.objects.get(tweet_id=status.in_reply_to_status_id)
            except:
                pass
                
        if status.retweeted_status:
            try:
                retweeted_status = Post.objects.get(tweet_id=status.retweeted_status.id)
                retweeted_status.retweets.add(obj)
                retweeted_status.save()
                obj.retweet = True
            except:
                pass

        obj.content=expand_urls(status.text)
        obj.pub_date = status.created_at
        obj.save()
    
    return True
    
