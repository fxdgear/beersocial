BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "nick"
BROKER_PASSWORD = "d3n4lirulz"
BROKER_VHOST = "/"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("core.tasks", )
CARROT_BACKEND = "django"