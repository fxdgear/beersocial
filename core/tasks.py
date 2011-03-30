from twython import Twython 
import email, datetime
import pytz

from posts.models import Post
from celery.decorators import periodic_task, task
from celery.task.schedules import crontab

@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*")) 
def get_new_tweets():
    twitter = Twython()  
    results = twitter.searchTwitter(q="#kubball, #lawrence")

    tweets = results['results']
    
    for tweet in tweets:
        utctimestamp = email.Utils.mktime_tz(email.Utils.parsedate_tz( tweet['created_at'] ))
        utcdate= datetime.datetime.fromtimestamp( utctimestamp, pytz.utc )
        tweet_date = utcdate.astimezone(pytz.timezone('US/Central'))
       
        obj,created = Post.objects.get_or_create(tweeter_id=tweet['from_user_id'], 
                                                 tweet_id=tweet['id'], 
                                                 pub_date=tweet_date)

        if created:
            obj.content=tweet['text']
            obj.tweeter_name=tweet['from_user']
            obj.tweeter_profile_image=tweet['profile_image_url']
            obj.save()