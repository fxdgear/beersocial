from beersocial.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'socialbeer',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'd3n4lirulz',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TWITTER_CONSUMER_KEY = 'u4Tf4AMzQ720A4Tb0tC7Q'
TWITTER_CONSUMER_SECRET_KEY = 'Ult77YdpQNu5opCiZrs4Otxl5Sbf3ttENXWUMN4MPU'
TWITTER_ACCESS_TOKEN = "5187401-PK1rSWelpqEgM6zpgMuZ0VxffpLlCFoLOriDJH74OA"
TWITTER_ACCESS_TOKEN_SECRET = "BM8q6sn7Vmt51iUNpUYiBmEam74RGxCj7N8UI2K7aE"
TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
TWITTER_AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "nicholas"
BROKER_PASSWORD = "d3n4lirulz"
BROKER_VHOST = "/"

CARROT_BACKEND = "django"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4trz8fd%fw1f8!5e+^$_nbl+=1u$2p7p9e6121(w)o5l&dy(3d'