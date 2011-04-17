from tweepy.api import API

from celery.decorators import task

@task()
def update_twitter_profile( *args, **kwargs):
    a = API()
    user = kwargs.get['instance']
    profile = user.get_profile()
    twitter_user = a.get_user(user_id=profile.twitter_profile.twitter_id)
    
    profile.user.first_name = twitter_user.name.split(" ")[0]
    profile.user.last_name = twitter_user.name.split(" ")[1:]
    profile.user.save()    

    profile.website = twitter_user.url    
    profile.profile_image_url = twitter_user.profile_image_url    
    profile.description = twitter_user.description    
    profile.twitter_name = twitter_user.screen_name
    profile.save()