from django.core.management.base import BaseCommand, CommandError
import time
from getpass import getpass

import tweepy

from django.conf import settings

from socialbeer.core.tasks import process_tweet

USERNAME = getattr(settings, "TWITTER_USERNAME", None)
PASSWORD = getattr(settings, "TWITTER_PASSWORD", None)
TRACK_LIST = getattr(settings, "TWITTER_SEARCH_TERMS", None)
FOLLOW_LIST = None

class Command(BaseCommand):
    def handle(self, *args, **options):
        stream_twitter()


class StreamWatcherListener(tweepy.StreamListener):

    def on_status(self, status):
        process_tweet(status)
        return True
        

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def stream_twitter():
    # Prompt for login credentials and setup stream object
    stream = tweepy.Stream(USERNAME, PASSWORD, StreamWatcherListener(), timeout=None)
    mode = 'filter'

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
        stream.filter(FOLLOW_LIST, TRACK_LIST)


if __name__ == '__main__':
    try:
        stream_twitter()
    except KeyboardInterrupt:
        print '\nGoodbye!'

